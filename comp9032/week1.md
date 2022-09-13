<!-- SPDX-License-Identifier: zlib-acknowledgement -->

ATmega2560

pass-through only available for linux-linux
virtual-hardware-details➞ add-hardware➞ file-system

for windows 10 samba IP is $(ifconfig) virbr0; also have to chmod +x .exe
use codeshare.io for basic code sharing

'data path' is from registers to execution units

for adding, require at most 1 extra bit than max bit number for carry
for multiplying, as many bits as both number of bits in each added together

adding binary know how to carry
subtracting binary know how to borrow (however, if convert to twos complement can just add, e.g. a + b = a + (-b))
multiplying, shift over each place

carry flag if incorrect unsigned interpretation
overflow flag if incorrect signed interpretation
(common bits in a status register, as well as zero flag; perhaps also interrupts?)

AVR is very close to actual Harvard, with instructions and data in separate address spaces.
however, can read data from instruction address space with special instructions, so still modified Harvard.

16-bits addressable:
data memory also contains constants (SRAM)
program memory (Flash) (jmp, call instructions)

ISA will include memory model, addressing modes, address spaces (one for program, one for data), native data types (e.g. 8 bit unsigned ints, 32 bit floating point)
ISA also specifies endianness and alignment?

8-bit (register sizes?) RISC

* segment vs section?
with microchip studio toolchain, .cseg/.dseg/.eseg
* understand alignment!. AVR word size of 16bits? aligned to 16bits?
* AVR is family of MCUs so doesn't exist in isolation? (I believe so as instruction set reference contains I/O registers)
* RISC, yet most instructions take 1 cycle? Load and
* Special instructions for XRAM in block diagram?
