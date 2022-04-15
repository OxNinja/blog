---
title: "🏌️ Binary golfing - Introduction"
date: 2022-04-15 16:00:00
tags: ["binary", "elf", "golf", "low-level"]
series: ["Binary golfing"]
author: "0xNinja"
showToc: true
TocOpen: false
draft: true
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
    image: cover.png
---

> So [tmp.out](https://tmpout.sh) - once again - got me. Especially [netspooky](https://n0.lol/), wich wrote about golfing binaries. Instantly I was caught in golfing.

## Binary golfing?

Crafting the smallest binary which does a particular task.

**Why someone would do this?**

* Learn about binary executables and format parsers
* Flex on muggles

## My notes on ELF format

It is recommanded to code in assembly in order to manage your headers as you wish.

We can handcraft binaries, because `GCC` is a bit messy when compiling code ans linking stuff. We can then make sections or headers overlap to save more space.

> In brief, the section header table is for use by the compiler and linker, while the program header table is for use by the program loader.
> The program header table is optionnal and never present in practice, the section header table is also optional but always present.
> - Brian Raiter, "A Whirlwind Tutorial on Creating Really Teensy ELF Executables for Linux"


### Compile

**Classic way:**

```sh
nasm -f elf32 file.s
ld -m elf_i386 -nmagic file.o -o bin
```

**Better:**

To directly craft a binary: `nasm -f bin file.s`.

### Header

The smallest valid header I can think of might be:

```hex
7f45 4c46 01?? ???? ???? ???? ???? ????
0200 0300 0100 ???? dead beef 2c00 0000
???? ???? ???? ???? 3400 2000 0100 0000
???? ???? 0000 0008 0000 0008 !!!! !!!!
!!!! !!!! 0500 0000 0010 0000
```

Considering the following:

* `??`: garbage, so you can just use those bytes for shellcode
* `!!!! !!!!`: total size of the header, so it will depend on your code
* `dead beef`: address of the entrypoint

Here is a template I modified from [here, so all creds to the author](https://www.muppetlabs.com/~breadbox/software/tiny/teensy.html):

```asm
bits 32

org 0x8000000

ehdr:                           ; Elf32_Ehdr
db 0x7F, "ELF", 1, 1, 1, 0      ; e_ident
times 8 db 0
dw 2                            ; e_type
dw 3                            ; e_machine
dd 1                            ; e_version
dd _start                       ; e_entry
dd phdr - $$                    ; e_phoff
dd 0                            ; e_shoff
dd 0                            ; e_flags
dw ehdrsize                     ; e_ehsize
dw phdrsize                     ; e_phentsize
dw 1                            ; e_phnum
dw 0                            ; e_shentsize
dw 0                            ; e_shnum
dw 0                            ; e_shstrndx

ehdrsize equ$ - ehdr

phdr:                           ; Elf32_Phdr
dd 1                            ; p_type
dd 0                            ; p_offset
dd $$                           ; p_vaddr
dd $$                           ; p_paddr
dd filesize                     ; p_filesz
dd filesize                     ; p_memsz
dd 5                            ; p_flags
dd 0x1000                       ; p_align

phdrsize equ$ - phdr

_start:

; your program here

filesize equ$ - $$
```

### Unethical stuff

#### Declaring variables in the wild

🙈 Nothing forbidens to declare variables anywhere, to save some space you can skip using the `.rodata` section.

```asm
section .text
	var: db "salut", 0xa
```

#### Use header as code section

**🧠** big brain move here: put code in the header

```asm
ehdr:
	db 0x7f, "ELF"
	db 1, 1, 1, 0, 0
_start:
	mov bl, 42
	xor eax, eax
	inc eax
	int 0x80
	;; continue le header
	dw 2
	dw 3
	dw 1
	;; ...
```

### Golfing resources

https://codegolf.stackexchange.com/questions/5696/shortest-elf-for-hello-world-n
[Create tiny ELF for Linux](https://www.muppetlabs.com/~breadbox/software/tiny/teensy.html)
https://www.muppetlabs.com/~breadbox/software/tiny/
[Analyzing ELF with malformed headers](https://binaryresearch.github.io/2019/09/17/Analyzing-ELF-Binaries-with-Malformed-Headers-Part-1-Emulating-Tiny-Programs.html)
