;
; Lab3_Task3.asm
;
; Created: 2018/9/18 19:52:11
; Function: This program performs multiplication: a = b x c, 
; where a, b, c are all unsigned 1-byte integers. 
; The program takes b and c from the keypad and displays the result on the LED bar.
; When there is an overflow in the calculation, the LED bar flashes 3 times.

.include "m2560def.inc"

.def row   = r16				; current row number
.def col   = r17				; current column number
.def rmask = r18				; mask for current row during scan
.def cmask = r19				; mask for current column during scan
.def temp1 = r20  
.def temp2 = r21

.def M1   = r22					; 
.def M2   = r23					; 
.def ten  = r24					; 
.def flag = r25					; for judge before* or after* 

.equ PORTFDIR = 0xF0			; use PortF for input/output from keypad: PF7-4,output; PF3-0,input.
.equ ROWMASK  = 0x0F			; low four bits are output from the keypad. This value mask the high 4 bits.

.equ INITCOLMASK = 0xEF			; scan from the leftmost column, the value to mask output
.equ INITROWMASK = 0x01			; scan from the bottom row


.macro  HalfSecondDelay					; Half Second Delay loop

		ldi r16, 0x00					; 1, load 0x00 to r16
		ldi r17, 0x35					; 1, load 0x35 to r17
		ldi r18, 0x0c					; 1, load 0x0c to r18
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

.macro  flash							; for flash use
		out PORTC, @0					 
		HalfSecondDelay					
		out PORTC, @1					 
		HalfSecondDelay
.endmacro


RESET:
		ldi temp1, PORTFDIR				; 0xf0 to temp1
		out DDRF, temp1					; columns are outputs, rows are inputs

		ser temp1						; set temp1
		out DDRC, temp1					; Port C is outputs
		out PORTC, temp1				; initialize to ff

		ldi ten, 10						; load 10 to r24
		ldi M1, 0						; initialize M1 to 0
		ldi M2, 0						; initialize M2 to 0
		ldi flag, 0						; initialize flag to 0
		ldi r27, 0xff					; initialize r27 to FF

main:
		ldi cmask, INITCOLMASK			; initial column mask
		clr col							; initial column

colloop:
		cpi col, 4						; compare clo with 4
		breq main2						; if all keys are scaned, jump to main2 to continue the program
		jmp continue

main2:
		ldi r27,0xff					; all keys are released, set the value of r27 to 0xff
		jmp main						; if r27 don't reset, consecutive  value can not be input

continue:
		out PORTF, cmask				; set column to mask value (one column off)
		ldi temp1, 0xFF					; 0xff to temp1
delay:
		dec temp1						; temp1 - 1
		brne delay						; Branch to delay

		in temp1, PINF					; read PORTF, just for checking if there is any button pressed
		andi temp1, ROWMASK				; only 4 buttons,so mask high 4 bits
		cpi temp1, 0xF					; check if any rows are on, if is, represent no button is pressed
		breq nextcol					; Branch to next column

										; if yes, find which row is on
		ldi rmask, INITROWMASK			; initialise row check
		clr row							; initial row

rowloop:
		cpi row, 4						; compare row with 4
		breq nextcol					; Branch to nextcol
		mov temp2, temp1				; move temp2 to temp1
		and temp2, rmask				; check masked bit
		breq convert					; if bit is clear, convert the bitcode
		
		inc row							; else move to the next row
		lsl rmask						; shift the mask to the next bit
		jmp rowloop						; jmp to rowloop

nextcol:
		lsl cmask						; else get new mask by shifting and 
		inc col							; increment column value
		jmp colloop						; and check the next column

convert:
		cpi col, 3						; compare clo with 3
		breq ABCD						; Branch to ABCD
 
		cpi row, 3						; if row is 3 we have a symbol or 0
		breq symbols
										; otherwise we have a number from 1 to 9
		mov temp1,row					; move row number to temp1
		lsl temp1						; temp1 * 2
		add temp1, row					; temp1 * 2 + temp1 = row * 3
		add temp1, col					; add the column address to get the value
		subi temp1, -1					; temp1 = row * 3 + col + 1

		cp r27, temp1					; r27 is 0xff，会导致不能连续两次输入一样的数字
		breq displayM1					; Branch to displayM1
		mov r27, temp1					; move temp1 to r27

		cpi flag, 0						; compare flag with 0
		breq InputM10					; Branch to InputM10
		brne InputM20					; Branch to InputM20
 
InputM10:
		cpi M1, 0						; compare M1 with 0
		brne InputM11					; Branch to InputM11
		mov M1, temp1					; first time, M1 = 0, so temp1 to M1.
		jmp convert_end					; jmp to convert_end
 
InputM11:
		mul M1, ten						; M1 * 10
		mov M1, r0						; Move M1 to r0
		add M1, temp1					; add temp1 with M1
		mov temp1, M1					; Move M1 to temp1
		jmp convert_end					; jmp to convert_end

InputM20:
		cpi M2, 0						; compare M2 with 0
		brne InputM21					; Branch to InputM21
		mov M2, temp1					; Move M2 to temp1
		jmp convert_end					; jmp to convert_end

InputM21:
		mul M2, ten						; M2 * 10
		mov M2, r0						; Move M2 to r0
		add M2, temp1					; add temp1 with M2
		mov temp1, M2					; Move M2 to temp1
		jmp convert_end					; jmp to convert_end

symbols:
		cpi  col, 0						; check if we have a star
		breq star						; Branch to star
		cpi  col, 1						; or if we have zero
		breq zero						; Branch to zero
		cpi  col, 2						; if not, is hash
		breq hash						; Branch to hash

MM:
		mul M1, M2						; multiplt M1 with M2
		mov r26, r1						; r16 to r31, can be used for comparing with immediate
		cpi r26, 0						; compare r1 with 0, if r1 != 0, there is an overflow.
		brne flash3times				; branch for LED bar flash 3 times.

		mov temp1, r0					; move r0 to temp1
		jmp displayResult				; jmp to displayResult

star:
		ldi flag, 1						; set to star
		ldi r27, 0xff					; 0xff to r27
		ldi temp1, 0xff					; 0xff to temp1
		jmp convert_end					; jmp to convert_end

zero:
		ldi temp1, 0					; set to zero
		cp r27, temp1					; comprare r27 with temp1
		breq displayM1					; Branch to

		mov r27, temp1					; move temp1 to r27
		cpi flag, 0						; compare flag with 0
		breq InputM10					; Branch to InputM10
		brne InputM20					; Branch to InputM20
		
hash:
		cpi flag,0						; compare flag with 0
		breq displayM1					; Branch equal, jump to dispalyM1
		brne MM							; if not equal, M1 * M2

ABCD:
		ldi r27, 0xff					; 0xff to r27
		jmp main						; skip ABCD

convert_end:
		out  PORTC, temp1				; write value to PORTC
		jmp  main						; restart main loop

displayM1:
		cpi  flag, 0					; compare flag with 0
		brne displayM2					; Branch to displayM2
		out  PORTC, M1					; write value to PORTC
		jmp  main						; restart main loop

displayM2:
		out  PORTC, M2					; write value to PORTC
		jmp  main						; jmp to main

displayResult:
		out PORTC, temp1				; display Result 
		jmp displayResult				; keep status

flash3times:

		ldi temp1, 0xFF					; 0xff to temp1
		ldi temp2, 0x00					; 0x00 to temp2

		flash temp1,temp2				; flash 1
		flash temp1,temp2				; flash 2
		flash temp1,temp2				; flash 3

		mov temp1, r0					; move r0 to temp1
		jmp displayResult				; display Result







		