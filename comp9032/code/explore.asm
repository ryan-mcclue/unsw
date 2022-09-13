.include "m2560def.inc"

# TODO(Ryan): signed subtraction. sign-extension 

.def sum_i=r18
.def sum=r19

while_loop:
  clr sum_i
  clr sum
loop_test:
  cpi sum_i, 20
  brge exit_loop
  inc sum_i
  mov r20, sum_i
  mul r20, r20
  add sum, r20
  rjmp loop_test
exit_loop:


.def a=r16
.def b=r17

branching:
  cpi a, 1
  brlt less_than
  mov b, a
  ; NOTE(Ryan): rjmp 1 word size (16 bits)
  rjmp end_if
less_than:
  mov a, b
end_if:


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



main:
  ldi r16, 10
  ldi r17, 20
; IMPORTANT(Ryan): This is an add without carry. Might what to consider if approaching limit
  add r16, r17 

; X, Y, Z are register pairs?
; interesting status register storage bit 
