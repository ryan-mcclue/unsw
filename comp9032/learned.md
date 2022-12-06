<!-- SPDX-License-Identifier: zlib-acknowledgement -->
add/sub/compare with carry

signed/unsigned branches

simple conflict register pushing and larger stack usage

sub same as cmp

mul typically in two different output registers

carry is for unsigned arithmetic
overflow is for signed arithmetic

AVR does not save registers on interrupt, nor any software interrupt instruction
must preserve status register value inside interrupt to avoid nasty logic errors
Interrupt priorities purely based on memory order (unlike NVIC)

AVR has separations commonly merged in modern MCUs, 
e.g. lpm (almost harvard), out/ld (different instruction decoders)

Differing word-size/address and register size

Different sized instructions, e.g. ld 16-bit only index registers, lds 32-bit all registers, rcall/rjmp/call/jmp
