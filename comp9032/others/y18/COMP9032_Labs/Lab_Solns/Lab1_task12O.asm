; Comp9032_task1_2
; Lab1.asm
;
; Function: Calculating the greatest common divisor of two number: 
; (for minimun execution time)

.def a=r16          ;definition r16 to a
.def b=r17          ;definition r17 to b

    cp a,b          ;compare a with b
	breq end        ;if a==b, go to end
	brge choice     ;if a>b, go to choice
main:   
	sub b,a         ;b=b-a
	cp a,b          ;compare a with b
	brlo main       ;if a<b, go to main
	breq end        ;if a==b, go to end
choice:
    sub a,b         ;a=a-b
	cp a,b          ;compare a with b
	brlo main       ;if a<b, go to main
	brne choice     ;if a>b, go to choice      
end:
    rjmp end