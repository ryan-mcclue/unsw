;
; LAB2_1.asm
;
; Created: 2018/8/28 17:17:42
; Function: Converting a string to an integer

.include "m2560def.inc"
.def Ten = r25				; to store constant value 10

.cseg

s:	.db  "79345",0			;s[ ] = "12345"	

	; main 
	ldi   r16,low(s)
	ldi	  r17,high(s)
	ldi   r19,high(65535)
	rcall atoi				; Call function ¡®atoi¡¯ 
	movw  r27:r26,r21:r20	; Get the return result

end: 
	rjmp end				; end of main

atoi:
	; Prologue:
							; r29:r28 will be used as the frame pointer
	push YL					; Save r29:r28 in the stack
	push YH
	push r22
	push r23
	push r24				; Save registers used in the function body
	push Ten

	in YL, SPL				; Initialize the stack frame pointer value
	in YH, SPH
	sbiw Y, 4				; Reserve space for local variables and parameters.

	out SPH, YH				; Update the stack pointer to 
	out SPL, YL				; point to the new stack top 

	std Y+1, r17			; store s to data space Y+1/Y+2
	std Y+2, r16			; 
	; End of prologue

	; Function body  
	clr r21					; n high bytes
	clr r20					; n low bytes
	clr r24
	ldi Ten,10				; Initialize r25 to 10
							
	ldd ZL, Y+1				; r17:r16 to z
	ldd ZH, Y+2

loop:
	lpm r18,Z+				; load data from program memory
	cpi r18,0				; in case of out of range
	breq done				; branch equal
	cpi r18, 48				; compare with '0'
	brsh sahi				; branch same or higher
	rjmp done

sahi:
	cpi r18,57				; compare with '9'
	breq loeq				; branch equal
	brlo loeq				; branch lower
	rjmp done

loeq:
	cpi r20,low(65535)		; n compare with 65535, r21:r20 is n
	cpc r21,r19				; r19 is high(65535)
	breq func				; branch equal
	brlo func				; branch lower
	rjmp done

func:						; n = 10 * n + (c -'0')
	mul r20,Ten				
	movw r23:r22,r1:r0		; move r1:r0 to r23:r22
	mul r21,Ten				; mutiply r21 with 10
	add r23,r0				; 
	movw r21:r20,r23:r22	; move result to r21:r20
	subi r18, 48			; r18 - '0'
	add r20,r18				; add r20 with r18
	adc r21,r24				
	rjmp loop
	; End of function body

done:
	; Epilogue				; De-allocate the reserved space					
	adiw Y, 4
	out SPH, YH
	out SPL, YL
	pop Ten
	pop r24
	pop r23
	pop r22
	pop YH
	pop YL
	ret						; Return to main() 
	; End of epilogue
