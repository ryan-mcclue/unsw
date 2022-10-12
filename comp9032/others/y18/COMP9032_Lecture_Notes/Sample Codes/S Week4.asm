;
.include "m2560def.inc" 
.def zero = r15				; to store constant value 0 
.equ m = 2 
.equ n = 3 
; Macro mul2: multiplication of two 2-byte unsigned numbers with a 2-byte result 
; All parameters are registers, @5:@4 should be in the form: rd+1:rd, where d is 
; the even number, and rd+1:rd are not r1:r0 
; Operation: (@5:@4) = (@1:@0)*(@3:@2) 

.macro	mul2				; a * b 

		mul  @0, @2			; al * bl 
		movw @5:@4, r1:r0 
		mul  @1, @2			; ah * bl 
		add  @5, r0 
		mul  @0, @3			; bh * al 
		add  @5, r0 

.endmacro

	; main 
	ldi r22, low(m)			; m = 2 
	ldi r23, high(m) 
	ldi r20, low(n)			; n = 3 
	ldi r21, high(n) 
	rcall pow				; Call function ¡®pow¡¯ 
	movw r23:r22, r25:r24	; Get the return result 

end: 
	rjmp end				; end of main

pow:
	; Prologue:
							; r29:r28 will be used as the frame pointer
	push YL					; Save r29:r28 in the stack
	push YH
	push r16				; Save registers used in the function body
	push r17
	push r18
	push r19
	push zero

	in YL, SPL				; Initialize the stack frame pointer value
	in YH, SPH
	sbiw Y, 8				; Reserve space for local variables and parameters.

	out SPH, YH				; Update the stack pointer to 
	out SPL, YL				; point to the new stack top 

							; Pass the actual parameters 
	std Y+1, r22			; Pass m to b  ; store r22 in data space location Y+1 ?
	std Y+2, r23 
	std Y+3, r20			; Pass n to e 
	std Y+4, r21			
	; End of prologue

	; Function body 
							; Use r23:r22 for i and r25:r24 for p, 
							; r21:r20 temporarily for e and r17:r16 for b 
	clr zero 
	clr r23					; Initialize i to 0 
	clr r22
	clr r25					; Initialize p to 1 
	ldi r24, 1				; Store the local values to the stack 
							; if necessary 
	ldd r21, Y+4			; Load e to registers 
	ldd r20, Y+3 
	ldd r17, Y+2			; Load b to registers 
	ldd r16, Y+1

loop: 
	cp r22, r20				; Compare i with e 
	cpc r23, r21 
	brsh done				; If i >= e 
	mul2 r24,r25, r16, r17, r18, r19	; p *= b 
	movw r25:r24, r19:r18 
	;std Y+8, r25			; store p 
	;std Y+7, r24 
	inc r22					; i++, (can we use adiw?) 
	adc r23, zero 
	;std Y+6, r23			; store i 
	;std Y+5, r22
	 rjmp loop 

done: 
	; End of function body

	; Epilogue 
	adiw Y, 8				; De-allocate the reserved space 
	out SPH, YH 
	out SPL, YL 
	pop zero 
	pop r19 
	pop r18					; Restore registers 
	pop r17 
	pop r16 
	pop YH 
	pop YL 
	ret						; Return to main() 
	; End of epilogue