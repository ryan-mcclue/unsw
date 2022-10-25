<!-- SPDX-License-Identifier: zlib-acknowledgement -->

8 and 16bit timers
a timer is just a counter circuit, therefore require clock source
has various modes, e.g. counting direction, period, action on overflow, etc.

timer-period: ((timer-max)*(clock-prescaler))/(clock-hz)
8bit: (256 * 64)/(16MHz)

TODO: in ISRs load all values from RAM?
TODO: how to best architect timing requirements, e.g. this executes every 1 second, this every 500ms etc.  
