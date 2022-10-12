
; COMP9032 Lab1_Task2.asm

; Created: 12/08/2018
; Author: Juan Chen
; Version number: 3


.def	n = r19					; n is a 8-bit unsigned integer
.def    a = r20					; a is a 8-bit unsigned integer
.def	i = r21					; 
.def	sumL = r24				; define sumL to r24
.def	sumH = r25				; define sumH to r25
.def    bL = r22				; define bL to r22
.def    bH = r23				; define bH to r23
.def    cL = r16				; define cL to r16
.def    cH = r17				; define cH to r17

.macro  sumulate
		inc    i				; i+1
		mul    r22,a			; multiply r22 with a  
		movw   r17:r16,r1:r0	; move r1:r0 to r17:r16
		mul    r23,a			; multiply r23 with a 
		add    r17,r0			; add r17 with r0
		movw   r23:r22,r17:r16	; move r17:r16 to r23:r22
		add    sumL,r22			; add sumL with r22
		adc    sumH,r23			; add sumH with r23
.endmacro


main:
		ldi    i,1				; load 1 to i
		clr    sumL				; clear sumL
		clr    sumH				; clear sumH
		mov    r0,r20			; move r20 to r0
		add    sumL,r0			; add sumL with r0
		movw   r23:r22,r1:r0	; move r1:r0 to r23:r22

loop:
		cp     i,n				; compare i with n
		brsh   end				; if i>=n,go to end
		sumulate
		rjmp   loop				

end:
        rjmp   end
		


