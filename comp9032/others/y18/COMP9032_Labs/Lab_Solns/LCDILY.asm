
; Board settings: 
; 1. Connect LCD data pins D0-D7 to PORTF0-7.
; 2. Connect the four LCD control pins BE-RS to PORTA4-7.
  
.include "m2560def.inc"

.equ LCD_RS = 7
.equ LCD_RW = 5
.equ LCD_E  = 6
.equ LCD_BE = 4

.equ F_CPU = 16000000
.equ DELAY_1MS = F_CPU / 4 / 1000 - 4
; 4 cycles per iteration - setup/call-return overhead

.macro	do_lcd_command
		ldi   r16, @0
		rcall lcd_command
		rcall lcd_wait
.endmacro

.macro	do_lcd_data
		ldi   r16, @0
		rcall lcd_data
		rcall lcd_wait
.endmacro

.macro	lcd_set
		sbi PORTA, @0
.endmacro

.macro	lcd_clr
		cbi PORTA, @0
.endmacro


RESET:
		ldi r16, low(RAMEND)
		out SPL, r16
		ldi r16, high(RAMEND)
		out SPH, r16

		ser r16
		out DDRF, r16
		out DDRA, r16
		clr r16
		out PORTF, r16
		out PORTA, r16

		do_lcd_command 0b00111000 		; 2x5x7
		rcall sleep_5ms

		do_lcd_command 0b00111000 		; 2x5x7
		rcall sleep_1ms

		do_lcd_command 0b00111000 		; 2x5x7
		do_lcd_command 0b00111000 		; 2x5x7

		do_lcd_command 0b00001000 		; display off
		do_lcd_command 0b00000001 		; clear display
		do_lcd_command 0b00000110 		; increment, no display shift
		do_lcd_command 0b00001100 		; Cursor on, bar, no blink

		; set first line address
		do_lcd_command 0b10000000
		do_lcd_data 'L'
		do_lcd_data 'o'
		do_lcd_data 'v'
		do_lcd_data 'e'
		; set second line address
		do_lcd_command 0b11000000
		do_lcd_data 'Y'
		do_lcd_data 'o'
		do_lcd_data 'u'

halt:
		rjmp halt

; Send a command to the LCD (r16)
lcd_command:
		out PORTF, r16
		nop

		lcd_set LCD_E
		nop
		nop
		nop

		lcd_clr LCD_E
		nop
		nop
		nop
		ret

lcd_data:
		out PORTF, r16
		lcd_set LCD_RS
		nop
		nop
		nop

		lcd_set LCD_E
		nop
		nop
		nop

		lcd_clr LCD_E
		nop
		nop
		nop
		lcd_clr LCD_RS
		ret

lcd_wait:
		push r16
		clr r16
		out DDRF, r16
		out PORTF, r16
		lcd_set LCD_RW

lcd_wait_loop:
		nop
		lcd_set LCD_E
		nop
		nop
		nop
		in r16, PINF
		lcd_clr LCD_E
		sbrc r16, 7
		rjmp lcd_wait_loop
		lcd_clr LCD_RW
		ser r16
		out DDRF, r16
		pop r16
		ret

sleep_1ms:
		push r24
		push r25
		ldi r25, high(DELAY_1MS)
		ldi r24, low(DELAY_1MS)

delayloop_1ms:
		sbiw r25:r24, 1
		brne delayloop_1ms
		pop r25
		pop r24
		ret

sleep_5ms:
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		ret



