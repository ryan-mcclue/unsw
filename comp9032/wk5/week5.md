<!-- SPDX-License-Identifier: zlib-acknowledgement -->

IMPORTANT: if enable as input, the context of GPIO registers can change:
e.g. as output, PORT is written to to get ouput. conversely, if input, PORT is pull-up/down and PIN is used to read input

LCD display controllers will have some RAM, ROM and registers (IR to say display/clear, DR character, RS select which one)

Why go to a transceiver?

when interfacing with other hardware, will have timing/synchronisation
requirements, e.g. wait certain time for for write/read operations

Component hardware reset related to power supply load, so may not be reliable.
∴ implement in software

Interrupt signals can be level or edge triggered 
IRQ-FF holds pending interrupt request until acknowledged by Sequence Controller.
The Sequence Controller will acknowledge when current instruction has finished on CPU 

Non-maskable interrupt like RESET cannot be ignored
multiple sources of reset:
  * supply voltage below power-on reset threshold
  * external reset when low-level on reset pin
  * watchdog timer period expires 

AVR does not save any registers when transferring control to ISR 
AVR has no software interrupt instruction

AVR has external (tied to specific pins or pins can be configured) and internal interrupts (triggered by changes in internal AVR hardware)

global interrupt bit (disable for performance code) and local interrupt bit
by default, global interrupt bit cleared when inside an ISR (however can set to allow for nested)

priority of vectors determined by order of 2-word vectors (instruction to execute) in program memory
(indicated by interrupt vector table)
```
.cseg 0x0000
rjmp RESET
nop
jmp IRQ0
reti
nop
reti
nop
```
