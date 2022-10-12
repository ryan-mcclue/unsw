; COMP9032 Lab1_task1_1.asm

; Function: Calculating the greatest common divisor of two numbers: for minimum code size
; Created: 01/08/2018 15:46:27


.def	a = r16				;define a to be register r16
.def	b = r17				;define b to be register r17

loop:		
		cp   a,b			;Compare r16 with r17
		breq end			;if r16 = r17, go to end
		brlo else		    ;if r16 < r17, go to else
		sub  a,b			;subtract b from a and store the result in a
		rjmp loop

else:   sub  b,a			;subtract a from b and store the result in b
        rjmp loop

end:
        rjmp end
