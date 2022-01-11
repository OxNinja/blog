---
title: "🪛 Build your own mechanical keyboard"
date: 2021-10-02T13:00:28+02:00
summary: "A simple and quick summary on how to build a mechnical keyboard on your own from scratch."
tags: ["diy", "hardware"]
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
cover:
  image: cover.jpg
---

## Why?

Why not?

## Components

> I bought all the parts on [kbdfans.com](https://kbdfans.com), but you can find a lot of things on other websites. Be careful on the shipping tho!

| Part        | Product     | Comment     |
|-------------|-------------|-------------|
| Switches    | Gateron red | linear, x70 |
| Stabilizers | Cherry Screw-in Stabs 60 set |  |
| PCB         | KBD67 rev2 65% PCB | RGB, VIA support, USB-C |
| Plate       | Aluminium plate |  |
| Backplate   | TADA68 Low Profile Aluminum Case |  |
| Keycaps     | Generic caps |  |
| Lube        | PCMasterrace lube |  |

> Tip: buy a [lube station](https://kbdfans.com/products/kbdfans-lube-tools-collection-1) and a [switch disassembler](https://kbdfans.com/collections/switch-opener) for more confort

## Switches

First thing to do is to disassemble the switches and separate all the pieces for lubing.

![Disassembled](switch_disass.jpg)

![Switches lubing](switches_lubing1.jpg)

![Switches lubing](switches_lubing2.jpg)

![Switches lubing](switches_lubing3.jpg)

**Ref:**

{{< youtube 44Wv4OGdmu4 >}}

## Test the PCB

We want to test our PCB if any pin is damaged or not working, I used the [VIA software](https://github.com/the-via/releases/releases) to check it.

![PCB connected](pcb.jpg)

## Stabilzers

Trim the useless feet of the stabilizers for better stability and less noise.

| Before                     | After                    |
|----------------------------|--------------------------|
| ![Before](stab_before.jpg) | ![After](stab_after.jpg) |

Now we will lube the stabs and place them on the PCB.

**Ref:**

{{< youtube usNx1_d0HbQ >}}

## Soldering

We now want to solder the switches to the PCB.

![Soldering](solder.jpg)

**Ref:**

{{< youtube y5TZJ1nkUw8 >}}

## Finish

Put the keycaps on it and you got your brand new handmade keyboard.

![Assembled keyboard](assembled.jpg)

![Not much but honest work](https://i.kym-cdn.com/entries/icons/original/000/028/021/work.jpg)

## Sound testing

> Sorry for bad quality

| Keyboard                     | Sound             |
|------------------------------|-------------------|
| Ducky One 2 (MX brown)       | [mp3](k_duck.mp3) |
| Keychron k3 (MX brown lubed) | [mp3](k_keyc.mp3) |
| Mine (Gatheron red lubed)    | [mp3](k_mine.mp3) |

## Configure keyboard with VIA

[VIA](https://caniusevia.com/) is an open source software to help you configure your keyboard: adding layers (like Fn key), macros and so on.

I used it in order to add a function on my right control key, to unlock a new layer on the keyboard, I can now use F1-F10 keys easily.