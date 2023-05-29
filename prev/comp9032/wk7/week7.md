<!-- SPDX-License-Identifier: zlib-acknowledgement -->

8 and 16bit timers
a timer is just a counter circuit, therefore require clock source
has various modes, e.g. counting direction, period, interrupt on overflow, 
interrupt when matching against output compare register

timer-period: ((timer-max)*(clock-prescaler))/(clock-hz)
8bit: (256 * 64)/(16MHz)

TODO: in ISRs load all values from RAM?
TODO: how to best architect timing requirements, 
e.g. this executes every 1 second, this every 500ms etc.

PWM width;period;duty-cycle generated with counters
PWM requires low-pass filter (attenuates frequencies higher) to smooth inherent PWM noise
(the filter is in the devices used, e.g. motor?)

Pulse width directly proportional to output voltage.
higher voltage means motor goes faster 
fast-pwm 0-255 (higher frequencies; more commonly used) (count to max, then to 0)
phase-correct-pwm 0-255-0 (half frequency of fast-pwm)  (count to max, then decrement to 0)
(phase correct meaning timer slope up and slope down match as oppose to fast where slope up greater than vertical slope down)
(there will be a threshold value on timer slope corresponding to active)
