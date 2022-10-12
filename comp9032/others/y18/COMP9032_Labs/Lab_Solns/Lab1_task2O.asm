;
; Lab1_task2.asm
;
; Created: 2018/8/14 15:12:24
; Author : juan chen
; Version number: 2


.dseg							; start the data segment

n:			.byte 1				; n is 8-bit unsigned integer
a:			.byte 1				; a is 8-bit unsigned integer
aC:			.byte 1
bL:			.byte 1	
bH:			.byte 1				
sumL:		.byte 1			
sumH:		.byte 1				


.cseg							; start the code segment

		ldi		r16, 5			; load a number to r16
		sts		a, r16			; store r16 to a
		sts		bL, r16			; srore r16 to bL
		sts		sumL, r16		; srore r16 to sumL
		ldi		r16, 6			; load a number to r16
		sts		n, r16			; store r16 to n


.macro  calculate

		lds		r16, bL			; load bL to r16
		lds		r17, a			; load a to r17
		mul		r16, r17		; Multiply r16 and r17
		sts		bL, r0			; store r0 to bL
		sts		aC, r1			; store r1 to aC
		lds		r16, bH			; load bH to r16
		mul		r16, r17		; Multiply r16 and r17
		lds		r16, aC			; load aC to r16
		add		r16, r0			; add r16 with r0
		sts		bH, r16			; srore r16 to bH
		lds		r16, n			; load n to r16
		dec     r16				; r16-1
		sts		n,r16			; srore r16 to n

.endmacro


loop:
		lds		r16, n			; load n to r16
		cpi		r16, 1			; compare 1 with r16
		breq	END				; Branch if equal
		calculate				; call macro
		lds		r0, bL			; load bL to r0
		lds		r1, bH			; load bH to r1
		lds		r16, sumL		; load sumL to r16
		lds		r17, sumH		; load sumH to r17
		add		r16, r0			; add r16 with r0
		adc		r17, r1			; add with Carry 
		sts		sumL, r16		; srore r16 to sumL
		sts		sumH, r17		; srore r17 to sumH
		rjmp	loop			

END:
		lds		r16, sumL		; load sumL to r16
		lds		r17, sumH		; load sumH to r17
		nop
