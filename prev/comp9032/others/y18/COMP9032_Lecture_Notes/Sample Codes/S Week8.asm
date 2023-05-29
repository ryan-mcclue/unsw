
; Example of Initialization Code

.include “m2560def.inc” 

; General purpose register data stores value to be written to the LCD 
; Port F is output and connects to LCD
; Port A controls the LCD (Bit LCD_RS for RS and bit LCD_RW for RW, LCD_E for E). 
; The character to be displayed is stored in register data 
; Assume all labels are pre-defined. 
.macro  lcd_write_com 

		out PORTF, data 		; set the data port's value up 
		ldi temp, (0<<LCD_RS)|(0<<LCD_RW) 
		out PORTA, temp 		; RS = 0, RW = 0 for a command write 
		nop 					; delay to meet timing (Set up time) 
		sbi PORTA, LCD_E 		; turn on the enable pin 
		nop 					; delay to meet timing (Enable pulse width) 
		nop 
		nop 
		cbi PORTA, LCD_E 		; turn off the enable pin 
		nop 					; delay to meet timing (Enable cycle time) 
		nop 
		nop 
.endmacro

; Check LCD and wait until LCD is not busy
.macro  lcd_wait_busy 

		clr temp 
		out DDRF, temp 			; Make PORTF be an input port for now 
		out PORTF, temp 
		ldi temp, 1 << LCD_RW 
		out PORTA, temp 		; RS = 0, RW = 1 for a command port read 
		
busy_loop: 
		nop 					; delay to meet set-up time 
		sbi PORTA, LCD_E 		; turn on the enable pin 
		nop 					; delay to meet timing (Data delay time) 
		nop 
		nop 
		in temp, PINF 			; read value from LCD 
		cbi PORTA, LCD_E 		; turn off the enable pin 
		sbrc temp, LCD_BF 		; if the busy flag is set 
		rjmp busy_loop 			; repeat command read 
		clr temp 				; else 
		out PORTA, temp 		; turn off read mode
		ser temp 				
		out DDRF, temp 			; make PORTF an output port again 
.endmacro

; The del_hi:del_lo register pair store the loop counts 
; each loop generates about 1 us delay 
.macro 	delay

loop1: 
		subi del_lo, 1 
		sbci del_hi, 0 
		ldi r16, 0x3 
loop2: 
		dec r16 
		nop 
		brne loop2 
		brne loop1 				; taken branch takes two cycles. 
								; one loop iteration time is 16 cycles = ~1.08us 
.endmacro


		ldi del_lo, low(15000) 	;delay (>15ms) 
		ldi del_hi, high(15000) 
		delay 					; Function set command with N = 1 and F = 0 
								; for 2 line display and 5*7 font. The 1st command
								
		ldi data, LCD_FUNC_SET | (1 << LCD_N) 
		lcd_write_com 
		
		ldi del_lo, low(4100) 	; delay (>4.1 ms) 
		ldi del_hi, high(4100) 
		delay 
		lcd_write_com 			; 2nd Function set command
		
		ldi del_lo, low(100) 	; delay (>100 ns) 
		ldi del_hi, high(100) 
		delay 
		
		lcd_write_com 			; 3rd Function set command 
		lcd_write_com 			; Final Function set command 
		
		lcd_wait_busy 			; Wait until the LCD is ready 
		ldi data, LCD_DISP_OFF 
		lcd_write_com 			; Turn Display off 
		
		lcd_wait_busy 			; Wait until the LCD is ready 
		ldi data, LCD_DISP_CLR 
		lcd_write_com 			; Clear Display
		
		
		lcd_wait_busy 			; Wait until the LCD is ready 
								; Entry set command with I/D = 1 and S = 0 
								; Set Entry mode: Increment = yes and Shift = no 
		ldi data, LCD_ENTRY_SET | (1 << LCD_ID) 
		lcd_write_com 
		lcd_wait_busy 			; Wait until the LCD is ready 
								; Display On command with C = 1 and B = 0 
		ldi data, LCD_DISP_ON | (1 << LCD_C) 
		lcd_write_com
		
		
		
		
		