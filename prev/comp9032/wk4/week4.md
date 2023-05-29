<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Pullup/down refer to when pin is disconnected from input.
When using GPIO input, consider pull-up/down resistor
IMPORTANT: Although enabling internal resistors, 
must look at board schematic as external resistors might overrule

Button debouncing in hardware with NAND latch or in software with counter?

For a switch array, can feed into a multiplexor

Switch matrix will have say rows as Vcc and columns to switches. 
Will have diodes to prevent ghosting?

column output, 0 to select, 0 if down
row input, 1 to select, 1 if down

Vdd (drain, power supply to chip)
Vcc (collector, subsection of chip, i.e. supply voltage of circuit)
Vss (sink, ground)
Vee (emitter, ground)
