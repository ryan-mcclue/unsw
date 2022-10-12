; COMP9032 Lab1_task1_2.asm

; Function: Calculating the greatest common divisor of two numbers£ºfor minimum execution time
; Created: 08/08/2018 15:56:20  


.def	 a = r16			 ;define a to be register r16
.def	 b = r17			 ;define b to be register r17

loop:		
		 cp    a,b			 ;Compare a with b
		 brlo  LOchoice      ;if a < b, go to LOchoice

SHchoice:
         breq  end			 ;if a = b, go to end
         sub   a,b			 ;subtract b from a and store the result in a
		 cp    a,b           ;Compare a with b
		 brsh  SHchoice      ;if a >= b, go to SHchoice

LOchoice:
         sub   b,a           ;subtract a from b and store the result in b
		 cp    a,b			 ;Compare a with b
		 brlo  LOchoice		 ;if a < b, go to LOchoice
		 brsh  SHchoice		 ;if a >= b, go to SHchoice

end:    
         rjmp end
