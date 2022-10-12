;
; LAB3_task2O.asm
;
; Function: Using an external interrupt to start and stop LEDs¡¯ display.

; Replace with your application code
.include"m2560def.inc"

.def a = r16
.def count1 = r18		; 0xFF
.def count2 = r19		; 0x69
.def count3 = r20		; 0x18,1599999

.def flag = r22
.def M1 = r24
.def M2 = r25
.def temp = r17

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
		rjmp loop						; 2, (16000000-12)/10 = 1599998.8
done:
.endmacro

		jmp	RESET						; Jump to RESET to initialize interrupt
.org	INT0addr                        ; Initialize INT0 address
		jmp EXT_INT0                    ; Jump to external interrupt
.org    INT1addr
		jmp EXT_INT1		
				
RESET:
		ser temp
		ldi temp, (2 << ISC00)|(2 << ISC10)       ; Set INT0 as falling edge triggered interrupt
		sts EICRA, temp                 		  ; Store the value of temp to EICRA

		in temp, EIMSK                  		  ; Enable INT0
		ori temp, (1 << INT0)|(1 << INT1)         ; Logical OR register with immediate
		out EIMSK, temp							  ; Store data from r17 to EIMSK

		sei										  ; Enable global interrupt
		jmp main						
		
EXT_INT0:
		push temp						; Save register
		in	 temp, SREG                 ; Save SREG
		push temp                       ; 

		ldi  flag,0	 
		pop temp                        ; Restore SREG
		out SREG,temp                   ; Store data from r17 to SREG
		pop temp                        ; Restore register
		reti                            ; Return from the interrupt	

EXT_INT1:
		push temp						; Save register
		in	 temp, SREG                 ; Save SREG
		push temp                       ; 

		ldi  flag,1	 
		pop temp                        ; Restore SREG
		out SREG,temp                   ; Store data from r17 to SREG
		pop temp                        ; Restore register
		reti 		

main:
		cbi DDRD,1						; set Port D bit 0 for input
		cbi DDRD,0
		ser r21							; set register
		out DDRC,r21					; set Port C for output
		out PORTC,r21					; active the pull up
		ldi flag, 0

P1:
		ldi r21,0x44					; write the pattern£¨01000100£©
		out PORTC,r21					; output the pattern1
		OneSecondDelay					; delay
switch1:
		sbic PIND,1						; check if that bit is clear ; if yes skip the next instruction
		rjmp P2							; rjmp to p2
		rjmp switch1					; rjmp to switch1
	
P2:
		ldi r21,0x22					; write the pattern£¨00100010£©
		out PORTC,r21					; output the pattern2
		OneSecondDelay					; delay
switch2:
		sbic PIND,1						; check if that bit is clear ; if yes skip the next instruction
		rjmp P3							; rjmp to p3
		rjmp switch2					; rjmp to switch2

P3:
		ldi r21,0xFF					; write the pattern£¨11111111£©
		out PORTC,r21					; output the pattern3
		OneSecondDelay					; delay
switch3:
		sbic PIND,1						; check if that bit is clear ; if yes skip the next instruction
		rjmp P1							; rjmp to p1
		rjmp switch3
					
