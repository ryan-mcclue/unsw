<!-- SPDX-License-Identifier: zlib-acknowledgement -->

IMPORTANT: stack not necessary for recursion unless local variables used

AVR imposes a stack bottom of 0x0200

Caller sets up parameters (registers or stack?) and pushes return address on stack.

Each stack frame will have a localised version of a SP, i.e. a stack frame pointer
Use Y register (Z is for LPM)
The callee prologue (space for local variables) and subsequent cleanup epilogue
TODO: Why are function parameters last on stack frame?

AVR has both
memory-mapped IO (simple; possibly slower as address decoder has to decode entire address bus) 
first 64 IO registers mapped to 0x0020 - 0x01ff
and 
separate-address-space IO (special IN/OUT instructions required)
first 64 IO registers with separate addresses 0x00 - 0x3f

Synchronisation between IO and CPU required. 
In software, typically done with a status register

Parallel port can move a set of bytes on different lines at the same time, 
i.e simulatenous streams of data

Ports typically have a series of registers associated with them, e.g. data register
Ports can only be configured as output or input via data direction register? 
If input, must enable a pull-up or pull-down resistor?

Various logic units: adder, multiplexor, decoder, 
multioperational (e.g. performs AND/OR/NOT etc. like ALU),
latch (store information; level-triggered, i.e. when reaches particular value), 
flip-flop (clock edge-triggered latch, i.e. when rising/falling), 
registers (collection of flip-flops storing multi-bit values), 
counters (changes value every clock cycle)

* Why does AVR CALL push 3 bytes?
* RET seems to be an instruction; so more efficient than POP, JMP equivalents?
