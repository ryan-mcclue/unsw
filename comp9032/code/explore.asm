.include "m2560def.inc"

; IMPORTANT(Ryan): As the name implies, PUSH will put data at the next address to what the SP currently is at.
; POP will take value at current SP

; WinAVR a possible calling convention

; Stack pointer is a I/O register
; Seems we can access first 64 I/O with IN/OUT 1byte addresses (faster?). 
; Or can access all (64 + 416) with ST/LD 2byte addresses? Use ST/LD for SRAM access as well?

; TODO(Ryan): Pass parameters as registers. Then inside function assign parameters to stack and reuse those registers?
; If we treat everything as a function, then never have to save registers assuming stack size isn't an issue?
; The registers we use here are call-clobbered

; However can just do simple if we know not using large number of registers
simple_func:
  push r16
  push r17
  ; use freely
  pop r17
  pop r16
  ret

; IMPORTANT(Ryan): Function call
function:
; 1. SAVE STACK FRAME POINTER 
  push YL
  push YH
; 2.1 SETUP STACK FRAME
  rcall . ; equivalent to pushing 2 bytes
  push 0
  in YL, SPL
  in YH, SPH
; 2.2 SETUP STACK FRAME
  in YL, SPL
  in YH, SPH
  sbiw YH:YL, 3  
  out SPL, YL
  out SPH, YH
; 3. LOAD PARAMETERS ONTO STACK
  std Y+3, r16
  std Y+4, r17
; 4. ASSIGN LOCAL VARIABLES
  ldi r24, lo(10)
  std Y+1, r24 
  ldi r24, lo(20)
  std Y+2, r24 
; 5.1 CLEANUP STACK FRAME
  pop 0
  pop 0
  pop 0
  pop YH
  pop YL
; 5.2 CLEANUP STACK FRAME
  adiw Y, 8
  out SPL, YL
  out SPH, YH
  pop YH
  pop YL
; 6. RETURN
  ret


; IMPORTANT(Ryan): Will have particular compares for signed and unsigned
; multiplication output goes to multiple registers

.def sum_i=r18
.def sum=r19

; IMPORTANT(Ryan): So, 16bit address space.
; Unique to program memory is that it's arranged with 'word addresses', i.e. each address holds 16bits (in contrast to normal byte addresses)
; We pass in say 0x0000 as a byte address, but must convert to word-address equivalent, i.e. addr*2, addr*2+1
; so, special address semantics when working with program memory

; interesting status register storage bit 
.macro copy_bit
  bst @1, @2
  bld @2, @3
.endmacro
; copy_bit r4, 2, r5, 3


.set struct_size (4 + 20 + 1)
; pointing to SRAM
.dseg
s1: .byte struct_size

; default is .cseg, which itself will have a default .org pointing to flash
.cseg
s1_constant_initialisers: .dw LWRD(123456)
                          .dw HWRD(123456)
                          .db "Ryan     ", 0
                          .db 75

; X, Y, Z are register pairs that allow automatic indirect referencing, e.g. ld r16, X 
ldi r30, LOW(1000) ; zl
ldi r31, HIGH(1000) ; zh
ld r24, Z

.set modifiable=HIGH(10 + 10)
.equ fixed=(10 + 10) 

word_addition:
  ldi r16, LOW(300)
  ldi r17, HIGH(300)
  ldi r18, LOW(600)
  ldi r19, HIGH(600)
  ; IMPORTANT(Ryan): Add with carry 
  add r16, r18
  adc r17, r19 ; replace with sbc for subtraction
  ; IMPORTANT(Ryan): signed subtraction vs subtraction just means
  ; number range is reduced. same instructions?
end_loop:
  rjmp end_loop

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



