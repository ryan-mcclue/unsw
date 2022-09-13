.include "m2560def.inc"

.def hi = r20

; NOTE(Ryan): f(x) = 2x - xy - x²  
; IMPORTANT(Ryan): Typically use r16-r31 for more instruction applicability (due to 16bit instruction encoding)
three_dimensional_function:
  ldi r16, 2  
  mul r16, r2
  mov r17, r3
  mul r17, r4
  mov r18, r2
  mul r18, r18
  sub r16, r17
  sub r16, r18

; rjmp 1 word size (16 bits)


main:
  ldi r16, 10
  ldi r17, 20
; IMPORTANT(Ryan): This is an add without carry. Might what to consider if approaching limit
  add r16, r17 

; X, Y, Z are register pairs?
; interesting status register storage bit 
