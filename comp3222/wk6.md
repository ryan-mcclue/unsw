<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Digital systems have datapath (adders, muxes, registers, decoders etc.) 
which feed into controller (FSM) that feeds back into datapath.
(these datapath elements are often components like shiftleft, mux, downcnt etc.)

This is encoded in an algorithmic state machine (ASM).

Register Q outputs share bus through 3-state buffer.
So, controller asserts the control signal on buffer for output register.
and enable signal for input register.

More common to use muxes instead of 3-state buffers.
So, FSM will assert control signal of muxes to load data into registers.

include transitions, outputs and datapath activities.
```
S0: waiting for instruction
S1: Load rx from data
```
