.cseg
.org 0x0000
  jmp reset
.org 0x0008
  jmp isr
isr:
  reti

.org ...
reset:
  cli ;; clear global interrupt
