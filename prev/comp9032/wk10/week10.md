<!-- SPDX-License-Identifier: zlib-acknowledgement -->
"The External Interrupts are triggered by the INT0 and INT1 pins or any of the PCINT23...0 pins.
Observe that, if enabled, the interrupts will trigger even if the INT0 and INT1 or PCINT23...0 pins
are configured as outputs."

In other words, a program can trigger any one of these interrupts by writing to an interrupt-enabled pin. 
A "poor man's" Software Interrupt can be implemented by manipulating an otherwise-unused output pin.

For ADC, will have minimum (at least) and maximum (no reason for more) number of bits required for output resolution
