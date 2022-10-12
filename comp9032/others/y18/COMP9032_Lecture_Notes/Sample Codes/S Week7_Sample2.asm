.include “m2560def.inc” 
.include “my_macros.inc”

.def temp =r16
.def output = r17
.def count = r18
.equ PATTERN = 0b01010101 
.equ OVERFLOW = 0b11111111

	 rjmp RESET 
.org INT0addr
	 rjmp EXT_INT0
.org INT1addr
	 jmp EXT_INT1

RESET:
		ser temp
		out DDRC, temp
		ldi output, PATTERN 
		out PORTC, temp
		ldi temp, 0b00000010 
		out DDRD, temp
		out PORTD, temp

		ldi temp, (2 << ISC00) | (2 << ISC10)
		sts EICRA, temp

		in temp, EIMSK
		ori temp, (1<<INT0) | (1<<INT1)
		out EIMSK, temp

		sei
		jmp main

EXT_INT0:
		push temp
		in temp, SREG 
		push temp

		com output
		out PORTC, output 
		inc count

		pop temp
		out SREG, temp 
		pop temp
		reti

EXT_INT1:
		push temp
		in temp, SREG 
		push temp

		ldi output, OVERFLOW 
		out PORTC, output 
		oneSecondDelay

		ldi output, PATTERN 
		sbi PORTD, 1
		pop temp
		out SREG, temp 
		pop temp
		reti


main:
		clr count
		clr temp 
loop:
		inc temp
		cpi count, 0xFF 
		breq OV
		rjmp loop		
OV: 	
		cbi PORTD, 1
		clr count 
		rjmp loop

