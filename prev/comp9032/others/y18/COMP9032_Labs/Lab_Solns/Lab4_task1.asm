;
; Lab4_Task1.asm
;
; Created: 2018/10/01 19:52:11
; Function: Write an assembly program that displays characters inputted from the keypad 
; on the LCD. When the first line is full, the display goes to the second line.
; When the two lines are all full, the display is cleared and ready to display a new set of characters.

.include "m2560def.inc"
 
.def row    = r22			; current row number
.def col    = r23			; current column number
.def rmask  = r18			; mask for current row
.def cmask  = r19			; mask for current column
.def temp1  = r20  
.def temp2  = r21
.def flag   = r17

.equ PORTCDIR = 0xF0	 ; use PortC for input/output from keypad.
.equ ROWMASK  = 0x0F	 ; low four bits are output from the keypad. This value mask the high 4 bits.
.equ INITCOLMASK = 0xEF	 ; scan from the leftmost column, the value to mask output
.equ INITROWMASK = 0x01	 ; scan from the bottom row

.macro	do_lcd_command   ; initialize and set LCD
		ldi r16, @0
		rcall lcd_command
		rcall lcd_wait
.endmacro

.macro	do_lcd_data     ; write value to PORTF
		mov r16, @0
		rcall lcd_data
		rcall lcd_wait
.endmacro


RESET:
		ldi r30,0					; r30 as count
		ldi flag, 0					; for judge first or second line
		ldi temp1, PORTCDIR			; 0xF0 to temp1
		out DDRC, temp1				; columns are outputs, rows are inputs

		;lcd reset
		ldi r16, low(RAMEND)		; load 0xff to r16
		out SPL, r16				; 0xff to SPL
		ldi r16, high(RAMEND)		; load 0x21 to r16
		out SPH, r16				; 0x21 to SPH

		ser r16						; set r16
		out DDRF, r16				; set PORTF as output
		out DDRA, r16				; set PORTA as output
		clr r16						; clear r16
		out PORTF, r16				; PORTF to 0
		out PORTA, r16				; PORTA to 0

		do_lcd_command 0b00111000	; 2x5x7
		rcall sleep_5ms
		do_lcd_command 0b00111000	; 2x5x7
		rcall sleep_1ms
		do_lcd_command 0b00111000	; 2x5x7
		do_lcd_command 0b00111000	; 2x5x7
		
		do_lcd_command 0b00001000	; display off
		do_lcd_command 0b00000001	; clear display
		do_lcd_command 0b00000110	; increment, no display shift
		do_lcd_command 0b00001110	; display on/off, Cursor display on/off, cursor blink on/off

		
main:
		ldi cmask, INITCOLMASK	   ; initial column mask
		clr col					   ; initial column

colloop:
		cpi  col, 4				   ; compare column with 4
		breq allloop			   ; if equal, go to allloop 
		brne continue			   ; if all keys are scaned then repeat the scaning

allloop:  
		ldi r28,0xFF			   ; initial r28 if the key is not pressed 
		jmp main
		
continue: 
		out PORTC, cmask		   ; set column to mask value (one column off)
		ldi temp1, 0xFF

delay:
		dec  temp1					; decrease by 1
		brne delay

		in   temp1, PINC			; read PORTC
		andi temp1, ROWMASK			; 
		cpi  temp1, 0xF				; check if any rows are on
		breq nextcol
									; if yes, find which row is on
		ldi rmask, INITROWMASK		; initialise row check
		clr row						; initial row

rowloop:
		cpi  row, 4
		breq nextcol
		mov  temp2, temp1
		and  temp2, rmask			; check masked bit
		breq convert				; if bit is clear, convert the bitcode
		
		inc row						; else move to the next row
		lsl rmask					; shift the mask to the next bit
		jmp rowloop

nextcol:
		lsl cmask					; else get new mask by shifting and 
		inc col						; increment column value
		jmp colloop					; and check the next column

convert:
		cpi col, 3					; if column is 3 we have a letter
		breq letters    
		cpi row, 3					; if row is 3 we have a symbol or 0
		breq symbols

		mov temp1, row				; otherwise we have a number in 1-9
		lsl temp1
		add temp1, row				; temp1 = row * 3
		add temp1, col				; add the column address to get the value
		subi temp1, -'1'			; add the value of character '1',0x31
		jmp convert_end				; 

letters:
		ldi temp1, 'A'
		add temp1, row				; increment the character 'A' by the row value
		jmp convert_end

symbols:
		cpi col, 0					; check if we have a star
		breq star
		cpi col, 1					; or if we have zero
		breq zero     
		
		ldi temp1, '#'				; if not we have hash
		jmp convert_end

star:
		ldi temp1, '*'				; set to star
		jmp convert_end

zero:
		ldi temp1, '0'				; set to zero

convert_end:
		cp r28, temp1				; judge if there is a value in r28
		breq main					; if two values is equal to display 
		
		mov r28, temp1				; r28 tempeorly copy the first value
		do_lcd_data temp1			; write value to PORTF
		
		inc r30						; increase r30 by 1
		cpi r30, 16					; compare r30 with 16
		breq secondline				; branch to secondline
		jmp main					; restart main loop

secondline:
		
		cpi flag, 1					; compare flag wtih 0
		breq clear					; if flag equal 1, go to clear
		ldi r30, 0					; reset r30 as 0
		ldi flag, 1					; load 1 to flag
		do_lcd_command 0b11000000	; set second line address(0x40)
		jmp main

clear:
		do_lcd_command 0b00000001	; clear display
		ldi flag, 0					; reset flag to 0
		ldi r30, 0					; reset r30 to 0
		jmp main
		
halt:
		rjmp halt

.equ LCD_RS = 7						; 7 bit in PORTA
.equ LCD_E  = 6						; 6 bit in PORTA
.equ LCD_RW = 5						; 5 bit in PORTA
.equ LCD_BE = 4						; 4 bit in PORTA

.macro	lcd_set
		sbi PORTA, @0				; set bit in I/O register
.endmacro

.macro	lcd_clr
		cbi PORTA, @0				; clear bit in I/O register
.endmacro

; Send a command to the LCD (r16)

lcd_command:
		out PORTF, r16				; store data in r16 to PortF(connect to LCD)
		nop
		lcd_set LCD_E				; set bit 6 in PORTA(connect to LCD control)
		nop							; delay to meet timing
		nop
		nop
		lcd_clr LCD_E				; clear bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		ret	

lcd_data:
		out PORTF, r16				; store data in r16 to PortF(connect to LCD)
		lcd_set LCD_RS				; set bit 7 in PORTA(connect to LCD control)
		nop
		nop
		nop
		lcd_set LCD_E				; set bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		lcd_clr LCD_E				; clear bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		lcd_clr LCD_RS			    ; clear bit 7 in PORTA(connect to LCD control)
		ret

lcd_wait:
		push r16					; save r16
		clr r16						; clear r16
		out DDRF, r16				; set PortF as input
		out PORTF, r16				; clear PortF
		lcd_set LCD_RW				; set bit 5 in PORTA(connect to LCD control)

lcd_wait_loop:
		nop
		lcd_set LCD_E				; set bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		
		in r16, PINF				; load data from PINF to r16
		lcd_clr LCD_E				; set bit 6 in PORTA(connect to LCD control)
		sbrc r16, 7					; Skip if Bit in Register is Cleared
		rjmp lcd_wait_loop

		lcd_clr LCD_RW				; clear bit 5 in PORTA(connect to LCD control)
		ser r16						; set r16
		out DDRF, r16				; set PORTF as output
		pop r16
		ret

.equ F_CPU = 16000000
.equ DELAY_1MS = F_CPU / 4 / 1000 - 4
; 4 cycles per iteration - setup/call-return overhead

sleep_1ms:							; 1 ms delay
		push r24
		push r25
		ldi r25, high(DELAY_1MS)	; load high DELAY_1MS to r25
		ldi r24, low(DELAY_1MS)     ; load low DELAY_1MS to r25

delayloop_1ms:						; 1 ms delayloop 
		sbiw r25:r24, 1				; substract 1 from r25:r24
		brne delayloop_1ms			; if r25:r24 not equal 0, jump to delayloop_1ms
		pop r25
		pop r24
		ret

sleep_5ms:							; 5ms delay
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		ret



		