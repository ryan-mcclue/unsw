;
; Lab4_Task2.asm

; Created: 2018/10/01 13:22:00
; Function: Write an assembly program to control the motor operations. 
; When a button is pressed, the motor spins at its full speed. 
; When the button is pressed again, the motor stops.

.include "m2560def.inc"
.def Temp = r16	            ; define Temp to r16
.def del_lo = r18			; define del_lo to r18
.def del_hi = r19			; define del_hi to r19
.equ counter = 10

.macro  Delay					        ; Delay loop

		ldi r16, 0x00					; 1, load 0x00 to r16
		ldi r17, 0x35					; 1, load 0x35 to r17
		ldi r18, 0x02					; 1, load 0x0c to r18
		clr r19							; 1
		clr r24							; 1
		clr r25						    ; 1			
		clr r26						    ; 1
loop:
		cp   r24, r16					; 1 ,compare r24 with r16
		cpc  r25, r17					; 1 ,compare r25 with r17 with carry
		cpc  r26, r18					; 1 ,compare r26 with r18 with carry
		brsh done						; 1/2
		adiw r25:r24,1					; 2, add immediate to word
		adc  r26,r19					; 1, add with carry
		nop								; 1, do nothing
		rjmp loop						; 2, (8,000,000-12)/10 ~ 800,000  H: 0C3500
done:
.endmacro

reset:
		clr Temp				; clear Temp
		out DDRE, Temp			; set Port E as input
		jmp main

main:
		clr Temp				; clear Temp
		out PORTE, Temp			; out Temp to Port E

switch:
		delay
		sbic PIND, 1			; Skip if Bit in I/O Register is Cleared 
		rjmp main				; jump to main
		rjmp end				; jump to end

end:
		ser Temp				; set Temp
		out PORTE, Temp		    ; out Temp to Port E
		delay
		sbic PIND, 1			; Skip if push button is pressed
		rjmp end				; jump to end
		rjmp main				; jump to main







