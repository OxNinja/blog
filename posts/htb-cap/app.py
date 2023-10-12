#!/usr/bin/python3

import os
from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import tempfile
import dpkt
from werkzeug.utils import append_slash_redirect

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = b'\x81\x02&\x18\\a0ej\x06\xec\x917y*\x04Y\x83e\xebC\xee\xab\xcf\xac;\x8dx\x8bf\xc4\x15'
limiter = Limiter(app, key_func=get_remote_address, default_limits=["99999999999999999 per day", "99999999999999999999 per hour"])
pcapid = 0
lock = False

@app.before_first_request
def get_file_id():
        global pcapid
        path = os.path.join(app.root_path, "upload")
        onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        ints = []
        for x in onlyfiles:
                try:
                        ints.append(int(x.replace(".pcap", "")))
                except:
                        pass
        try:
                pcapid = max(ints)+1
        except:
                pcapid = 0


def get_appid():
        global pcapid
        return pcapid

def increment_appid():
        global pcapid
        pcapid += 1

def get_lock():
        global lock
        while lock:
                pass
        lock = True

def release_lock():
        global lock
        lock = False

def process_pcap(pcap_path):
        reader = dpkt.pcap.Reader(open(pcap_path, "rb"))
        counter=0
        ipcounter=0
        tcpcounter=0
        udpcounter=0

        for ts, pkt in reader:
                counter+=1
                eth=dpkt.ethernet.Ethernet(pkt)

                try:
                        ip=dpkt.ip.IP(eth.data)
                except:
                        continue

                ipcounter+=1

                if ip.p==0:
                        tcpcounter+=1

                if ip.p==dpkt.ip.IP_PROTO_UDP:
                        udpcounter+=1

        data = {}
        data['Number of Packets'] = counter
        data['Number of IP Packets'] = ipcounter
        data['Number of TCP Packets']  = tcpcounter
        data['Number of UDP Packets']  = udpcounter
        return data


@app.route("/")
def index():
        return render_template("index.html")

PCAP_MAGIC_BYTES = [b"\xa1\xb2\xc3\xd4", b"\xd4\xc3\xb2\xa1", b"\x0a\x0d\x0d\x0a"]

@app.route("/capture")
@limiter.limit("10 per minute")
def capture():

        get_lock()
        pcapid = get_appid()
        increment_appid()
        release_lock()

        path = os.path.join(app.root_path, "upload", str(pcapid) + ".pcap")
        ip = request.remote_addr
        # permissions issues with gunicorn and threads. hacky solution for now.
        #os.setuid(0)
        #command = f"timeout 5 tcpdump -w {path} -i any host {ip}"
        command = f"""python3 -c 'import os; os.setuid(0); os.system("timeout 5 tcpdump -w {path} -i any host {ip}")'"""
        os.system(command)
        #os.setuid(1000)

        return redirect("/data/" + str(pcapid))

@app.route("/ip")
def ifconfig():
	d = os.popen("ifconfig").read().strip()
	print(d)
	return render_template("index.html", rawtext=d)

@app.route("/netstat")
def netstat():
	d = os.popen("netstat -aneop").read().strip()
	print(d)
	return render_template("index.html", rawtext=d)

@app.route("/data")
def data():
        if "data" not in session:
                return redirect("/")
        data = session.pop("data")
        path = session.pop("path")
        return render_template("data.html", data=data, path=path)

@app.route("/data/<id>")
def data_id(id):
        try:
                id = int(id)
        except:
                return redirect("/")
        try:
                data = process_pcap(os.path.join(app.root_path, "upload", str(id) + ".pcap"))
                path = str(id) + ".pcap"
                return render_template("index.html", data=data, path=path)
        except Exception as e:
                print(e)
                return redirect("/")

@app.route("/download/<id>")
def download(id):
        try:
                id = int(id)
        except:
                return redirect("/")
        uploads = os.path.join(app.root_path, "upload")
        return send_from_directory(uploads, str(id) + ".pcap", as_attachment=True)

if __name__ == "__main__":
        app.run("0.0.0.0", 80, debug=True)
