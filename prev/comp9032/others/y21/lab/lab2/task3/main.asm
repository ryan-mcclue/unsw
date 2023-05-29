;
; led.asm
;
; Created: 10/7/2020 9:04:20 PM
; Author : izual
;
.include "m2560def.inc"

.def iH = r25
.def iL = r24
.def countH = r17
.def countL = r16
.equ loop_count = 50000

.macro halfSecondDelay
	ldi countL, low(loop_count)
	ldi countH, high(loop_count)
	clr iH
	clr iL
loop:
	cp iL, countL
	cpc iH, countH
	brsh done
	adiw iH:iL, 1
	clr r19				;6 cycles
	
innerloop:
	cpi r19, 30		;30*5 = 150	cycles
	brsh jmpout
	inc r19
	rjmp innerloop
jmpout:	
	nop
	nop
	rjmp loop		;4	cycles
done:				;160 cycles in total
.endmacro			;160 * 50000 = 8000000

main:
	ser r18 ;set all bits in r18 to 1
	out DDRC, r18 ;set port c for output
	;out DDRD, r18 
	;clr r18
	;out DDRD, r18 ;set port d for input
	cbi DDRD, 0 ;pb0

p1:
	ldi r18, 0x11 ;write pattern
	out PORTC, r18	
	halfSecondDelay
	
	sbis PIND, 0 ;push is 0 
	jmp p1_loop
p2:
	ldi r18, 0xAA
	out PORTC, r18
	halfSecondDelay
	
	sbis PIND, 0 ;
	jmp p2_loop
p3:
	ldi r18, 0x66
	out PORTC, r18
	halfSecondDelay
	
	sbis PIND, 0 ;
	jmp p3_loop
	rjmp p1

	

p1_loop:
	out PORTC, r18
	halfSecondDelay
	sbis PIND, 0
	jmp p1
	rjmp p1_loop

p2_loop:
	out PORTC, r18
	halfSecondDelay
	sbis PIND, 0
	jmp p2
	rjmp p2_loop

p3_loop:
	out PORTC, r18
	halfSecondDelay
	sbis PIND, 0
	jmp p3
	rjmp p3_loop
end:
	rjmp end
