
.equ size = 6
.def counter = r17
.dseg
.org 0x0200

ucase_string:	.byte size

.cseg
		ldi zh,high(lcase_string<<1)
		ldi zl,low(lcase_string<<1)

		ldi yh,high(ucase_string)
		ldi yl,low(ucase_string)
		clr counter

main:
		lpm		r20,z+
		subi	r20,32
		st		y+,r20
		inc		counter
		cpi		counter,size
		brlt	main

end:
		rjmp	end

lcase_string:	.db  "hello",0

