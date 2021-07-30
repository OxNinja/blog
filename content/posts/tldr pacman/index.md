---
title: "🚀 TL;DR - pacman"
date: 2021-05-04 13:00:00
summary: "The famous packet manager for Archlinux"
tags:
- archlinux
- pacman
- tldr
author: "0xNinja"
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: false
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

*I use Arch btw*

## `pacman`

The famous packet manager for Archlinux.

![Pacman](https://media.giphy.com/media/jxJjBMvqEvMSA/giphy.gif)

### Basic usage

```sh
pacman -S package # install package
pacman -R package # uninstall package
pacman -Syu # check for package updates
pacman -Q # list installed packages
pacman -Q word # list installed packages containing word
```

### Bonus

Nothing to do with `pacman`, but you can install packages from the [AUR repo](https://aur.archlinux.org/) too!

```sh
cd ~/.local/share
git clone aur_repo
cd aur_repo
makepkg -isc
```

[AUR packages](https://wiki.archlinux.org/title/Arch_User_Repository) are updated by the community and are meant to be built from source, in order to optimize the package for your machine.

### Resources

* https://archlinux.org/pacman/pacman.8.html
* https://wiki.archlinux.org/title/Pacman/Tips_and_tricks
