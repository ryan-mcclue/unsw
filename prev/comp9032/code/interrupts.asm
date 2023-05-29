.cseg
.org 0x0000
  jmp reset
.org 0x0008
  jmp int0
int0:
  reti

.org ...
reset:
  cli ;; clear global interrupt
; external
    sbi     EIMSK,INT0              ; enable int0
    lds     temp,EICRA
    sbr     temp,ISC00
    sts     EICRA,temp  ; set external interrupt control register to interrupt change
  sei

; pin specific
lds     temp,PCICR
        sbr     temp,(1 << PCIE1)
        sts     PCICR,temp
        lds     temp,PCMSK1
        sbr     temp,(1 << PC1)         ;enable pin-change interrupts for 1 (bank C)
        sts     PCMSK1,temp  
