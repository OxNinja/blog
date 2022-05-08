# How to install Archlinux


> :warning: Now Archlinux embeeds an install script which you can run with `archinstall`, this blog post is here for curious people wanting to know how to install things from scratch and know how a Linux system works.

> I recently installed Archlinux on my laptop, let me help you for a fresh new install, step by step, with all commands and tips I learnt.

After closing around 30-40 navigation pages on my phone after **every new installation**, I decided to take notes of my mistakes and the tips I learnt of my past experiences in this post.

Disclaimer: I based all my previous installations on the following, therefor some content will be very similar, if not the same.

* <https://archlinux.org/>
* <https://wiki.archlinux.fr/installation>
* <https://github.com/FredBezies/arch-tuto-installation/blob/master/install.md> (:fr:)
* <https://driikolu.fr/2020/03/install_arch_chiffre_uefi/> (:fr:)

I recommend to read [the tips](#tips) if you have an issue with something (`Ctrl-f` should work), or want to learn a bit more.

![noot noot](https://media.giphy.com/media/VygrnPyOOyTOU/giphy.gif)

## Archlinux

I really love the minimalist mindset of Archlinux: install only what you need and what you want. You need to change something in particular? You know how to do it because you learnt how to install it before.

You are in total control of your installation and can customize it as needed. Without mentioning the AUR packages.

## Bootable USB

The first thing to get is a USB stick to make it bootable and store the ISO on it.

```sh
sudo dd bs=4M if=/path/to/archlinux.iso of=/dev/sdX # sdX is your USB stick (see lsblk)
```

After some time, you get your USB bootable. Boot your computer on it to install Archlinux.

> :warning: I have an Nvidia graphics card (too recent to be supported) and needed to add the `nomodeset` flag on boot because of screen glitches.

## Base system

### Partitions

We first want to create our partitions. Make sure to get your disk label with `fdisk -l`.

We will create 4 partitions:

| Partition   | Name | Type  | Size            | Mount point     |
|-------------|------|-------|-----------------|-----------------|
| `/dev/sdX1` | EFI  | FAT32 | 128MiB          | `/mnt/boot/efi` |
| `/dev/sdX2` | Boot | ext4  | 256MiB          | `/mnt/boot`     |
| `/dev/sdX3` | Root | ext4  | 32GiB           | `/mnt`          |
| `/dev/sdX4` | Home | ext4  | Everything else | `/mnt/home`     |

> Those values are arbitrary, change them at your own risks.

```sh
# partitions
parted /dev/sdX
mklabel gpt
# EFI
mkpart primary fat32 1MiB 129MiB # 128MiB size
set 1 esp on
# Boot
mkpart primary ext4 129MiB 385MiB # 256MiB size
set 2 boot on
# Root
mkpart primary ext4 385MiB 32.4GiB # 32GiB size
# Home
mkpart primary ext4 32.4GiB 100% # take everything else
q
```

Create filesystem on the partitions:

```sh
mkfs.fat -F32 /dev/sdX1

for i in {2..4}; do mkfs.ext4 /dev/sdX$i; done # oneliner
# or
mkfs.ext4 /dev/sdX2
mkfs.ext4 /dev/sdX3
mkfs.ext4 /dev/sdX4
```

### Basic configuration

You want now to set your NTP:

```sh
timedatectl set-timezone Europe/Paris # change to your location
timedatectl set-ntp true
```

### Linux setup

**Basic install**

We will now mount our partitions on the system and install basic packages on it.

```sh
mount /dev/sdX3 /mnt
mkdir /mnt/home; mount /dev/sdX4 /mnt/home
mkdir /mnt/boot; mount /dev/sdX2 /mnt/boot
mkdir /mnt/boot/efi; mount /dev/sdX1 /mnt/boot/efi
```

> Reffer to [the partitions table](#partitions)

Let's install basic packages using `pacstrap`:

```sh
pacstrap /mnt base base-devel linux linux-firmware
```

> If your ISO is old, you will have to update your keyring because some PGP signatures could be missing/expired.

> You will want to add `nvidia` if you have such card. Or even your favourite text editor.

We can now generate our fstab:

```sh
genfstab -U /mnt >> /mnt/etc/fstab
```

> :warning: Do not forget to install `dhclient` if you want Internet access after reboot

**Configuration**

We can now edit our configuration:

```sh
vi /etc/hostname
# My-Super-Machine

vi /etc/hosts
# 127.0.0.1 My-Super-Machine.my-local-domain My-Super-Machine
```

```sh
# NTP setup
ln -sf /usr/share/zoneinfo/Europe/Paris /etc/localtime
hwclock --systohc
```

Set your locales:

```sh
vi /etc/locale.gen
# uncomment your locale
locale-gen

vi /etc/locale.conf
# Use your own
# LANG="en_US.UTF-8"
```

We can now set a password for the `root` account:

```sh
passwd
```

### Boot setup

Let's install Grub for the boot manager:

```sh
pacman -S grub efibootmgr
```

Setup the kernel modules and install Grub on the system:

```sh
arch-chroot /mnt
mkinitcpio -p linux

grub-install --target=x86_64-efi --efi-directory=/boot/efi --recheck /dev/sdX
grub-mkconfig -o /boot/grub/grub.cfg
```

Your system is now ready to work. Congratulations, you can now reboot the machine and unplug the USB stick!

### Sudoer user

We do not want to use `root` user, we create a sudo user:

```sh
useradd --create-home user_name
passwd user_name
usermod --append --groups wheel user_name
visudo
# uncomment %wheel ALL=(ALL) ALL
```

Users in `wheel` group will be sudoer (using their password).

![noot noot](https://media.giphy.com/media/VJCK9OYBxtdGo/giphy.gif)

## Graphical environment

You may now need to use a graphical environment, I will show how to use the famous i3 and setup a basic status bar: polybar.

> Install `xorg` if not installed yet

I will from now, exec commands as a regular user. `sudo -u user_name`.

### i3

```sh
sudo pacman -S i3-wm
```

And voilà, i3 is now installed. It will start on next login, we will see for a [connection manager](#lightdm) in a moment.

### polybar

You want a status bar? Polybar provide fast, easy to customize bars.

```sh
# not available on pacman repos, so build from source
cd ~/.local/share
git clone https://aur.archlinux.org/polybar
cd polybar; makepkg -isc
```

Once installed you can find cool themes at <https://github.com/adi1090x/polybar-themes> you will find installation and setup instructions on the repo.

You can add an entry for the bar to launch on login in your i3 config:

```sh
vim ~/.config/i3/config
# exec_always --no-startup-id ~/.config/polybar/launch.sh --your-selected-theme
```

### rofi

I use rofi for my application launcher and power menu, see <https://github.com/adi1090x/rofi> for more info.

Add a system bind on your config:

```sh
vim ~/.config/i3/config
# bindsym $mod+d exec ~/.config/rofi/launchers/launcher_you_want/launcher.sh
```

### lightdm

As its name says, lightdm is a lightweight package, it will allow you to setup your login page on startup.

Don't forget to enable it with sysytemd: `systemctl enable lightdm`.

## Post-installation troubleshouting

### BIOS update broke my setup

Yeah it appears that on a BIOS update, you can break your grub config. It happened to me every time as I run a dual boot alongside W*ndows. Jokes apart, it is very easy to fix things.

The main issue encountered is the disapearance of Grub and so, your Arch partition. Fear not, you can fix it in only 2 steps:

1. Find your bootable stick and boot on it
2. Follow the steps:

```sh
# mount your partitions
mount /dev/sdX3 /mnt; mount /dev/sdX4 /mnt/home; mount /dev/sdX2 /mnt/boot; mount /dev/sdX1 /mnt/boot/efi

# regenerate your fstab
genfstab -U /mnt >> /mnt/etc/fstab

# reinstall grub
arch-chroot /mnt
mkinitcpio -p linux
grub-install --target=x86_64-efi --efi-directory=/boot/efi --recheck
grub-mkconfig -o /boot/grub/grub.cfg
```

And you can reboot.

### Dual boot with windows

My grub did not detect my Windows partition, [this post](https://askubuntu.com/a/977251) helped me to solve the issue.

## Tips

* Something is broken? You forgot to install an important package but already completed all the steps? **Do not reinstall from scratch**! Just boot on your USB, mount your system back and `chroot` into it!
* If using Nvidia card, set `nomodeset` on boot if screen tearing/glitch
* Make sure to have some space for the root partition, even 32GB is tight sometimes
* Update your pacman's keyring if the ISO is old with `pacman-key --populate archlinux`
* Make sure to install `dhclient` and a network manager to access the Internet
* Disable the computer speaker BEEP: `echo blacklist pcspkr > /etc/modprobe.d/nobeep.conf`

If you find something broken here, feel free to send an issue on the Github repo.

As I am in some distro reinstallation process, I will update this notes on the fly.

