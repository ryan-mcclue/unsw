;
; LAB3_Task1.asm
;
; Created: 2018/9/4 15:28:16
; FUNCTION: Implement a LED control system to repeatedly display a sequence of three patterns,
; And the display will be halted when the user presses a button.

.include"m2560def.inc"

.def a = r16
.def count1 = r18		; 0xFF
.def count2 = r19		; 0x69
.def count3 = r20		; 0x18,1599999
.def M1 = r24
.def M2 = r25

.macro  OneSecondDelay
		ldi count1,	0xFF				; 1, load 0xff to r18
		ldi count2,	0x69				; 1, load 0x69 to r19
		ldi count3, 0x18				; 1, load 0x18 to r20
		clr r16							; 1
		clr r24							; 1
		clr r25							; 1			
		clr r26							; 1

loop:
		cp   M1,count1					; 1 ,compare M1 with count1
		cpc  M2,count2					; 1 ,compare M2 with count2 with carry
		cpc  r26,count3					; 1 ,compare r26 with count3 with carry
		brsh done						; 1/2
		adiw M2:M1,1					; 2, add immediate to word
		adc  r26,a						; 1, add with carry
		nop								; 1, do nothing
		rjmp loop						; 2
done:
.endmacro

        ;main
		cbi DDRD,0						; set Port D bit 0 for input
		sbi PORTD,0						; set Port D bit 0 to 1

		ser r21							; set register
		out DDRC,r21					; set Port C for output
		out PORTC,r21					; active the pull up					

P1:
		ldi r21,0x44					; write the pattern£¨01000100£©
		out PORTC,r21					; output the pattern1
		OneSecondDelay					; delay

switch1:
		sbic PIND,0						; check if that bit is clear ; if yes skip the next instruction
		rjmp P2							; rjmp to p2
		rjmp switch1					; rjmp to switch1

P2:
		ldi r21,0x22					; write the pattern£¨00100010£©
		out PORTC,r21					; output the pattern2
		OneSecondDelay					; delay

switch2:
		sbic PIND,0						; check if that bit is clear ; if yes skip the next instruction
		rjmp P3							; rjmp to p3
		rjmp switch2					; rjmp to switch2

P3:
		ldi r21,0xFF					; write the pattern£¨11111111£©
		out PORTC,r21					; output the pattern3
		OneSecondDelay					; delay

switch3:
		sbic PIND,0						; check if that bit is clear ; if yes skip the next instruction
		rjmp P1							; rjmp to p1
		rjmp switch3					; rjmp to switch3





