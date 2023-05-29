;
; COMP9032_18S2Project.asm
;
; Created: 2018/10/15 15:18:18
; Author : z5148637

.include "m2560def.inc"

.def row    = r19						; current row number
.def col    = r20						; current column number
.def rmask  = r21						; mask for current row
.def cmask  = r22						; mask for current column
.def temp1  = r23 
.def temp2  = r24
.def temp   = r25
.def score  = r17						; for score display
.def LED_control = r18					; for controlling LED dim light

.equ dim_light   = 32
.equ PORTCDIR    = 0xF0					; use PortC for input/output from keypad.
.equ ROWMASK     = 0x0F					; low four bits are output from the keypad. This value mask the high 4 bits.
.equ INITCOLMASK = 0xEF					; scan from the leftmost column, the value to mask output
.equ INITROWMASK = 0x01					; scan from the bottom row

.macro  TimeDelay						; R2 /24/25/26 /27/28/29

		ldi r27, 0xFF					; 1, load 0xff to r27
		ldi r28, 0x69					; 1, load 0x69 to r28
		ldi r29, 0x06					; 1, load 0x06 to r29,1599999
		clr r2							; 1, clear r16
		clr r24							; 1, clear r24
		clr r25							; 1, clear r25		
		clr r26							; 1, clear r26
loopp:
		cp   r24, r27					; 1 ,compare r24 with r27
		cpc  r25, r28					; 1 ,compare r25 with r28 with carry
		cpc  r26, r29					; 1 ,compare r26 with r29 with carry
		brsh done						; 1/2
		adiw r25:r24,1					; 2, add immediate to word
		adc  r26,r2						; 1, add with carry
		nop								; 1, do nothing
		rjmp loopp						; 2, (16000000-12)/10 = 1599998.8
done:
.endmacro

.macro  DisplayStart					; macro for display Start...
		do_lcd_command 0b00000001		; clear display
		do_lcd_data 'S'					
		do_lcd_data 't'
		do_lcd_data 'a'
		do_lcd_data 'r'
		do_lcd_data 't'
		do_lcd_data '.'
		do_lcd_data '.'
		do_lcd_data '.'
.endmacro


.macro	DimmedLight

		ldi LED_control, 0b00111000			; set PL3(OC5A)，PL4 (OC5B)，PL5 (OC5C) to output, 0b00111000	
		sts DDRL, LED_control

		ldi LED_control, @0					; connected to PL2 in lab board
		sts OCR5AL, LED_control				; store @0 to OCR5AL
		clr LED_control
		sts OCR5AH, LED_control				; clear OCR5A high bytes

		ldi LED_control, @0					; connected to PL3 in lab board
		sts OCR5BL, LED_control				; store @0 to OCR5BL
		clr LED_control
		sts OCR5BH, LED_control				; clear OCR5B high bytes

		ldi LED_control, @0					; connected to PL4 in lab board
		sts OCR5CL, LED_control				; store @0 to OCR5CL
		clr LED_control
		sts OCR5CH, LED_control				; clear  OCR5C high bytes

		ldi LED_control, (1 << CS50)		; set the Timer5 to Phase Correct PWM mode. 
		sts TCCR5B, LED_control
		ldi LED_control, (1 << WGM52)|(1 << WGM51)|(1<< WGM50)|(1<<COM5C1)|(1<<COM5B1)|(1<<COM5A1)
		sts TCCR5A, LED_control
.endmacro

.macro  FlashThreeTimes                      ; for flash use
		ldi temp1, 0x00
		ldi temp2, 0xFF						
		out PORTB, temp1					 							
		out PORTB, temp2					 
		TimeDelay
		out PORTB, temp1					 
		TimeDelay							
		out PORTB, temp2					 
		TimeDelay
		out PORTB, temp1					 
		TimeDelay
		out PORTB, temp2					 
		TimeDelay
		out PORTB, temp1					 							
.endmacro

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

.macro	do_lcd_score
		mov   r16, @0
		rcall lcd_data
		rcall lcd_wait
.endmacro

; Step1: 
; 1. After the simulation system is turned on (i.e. the lab board is powered on), 
; the system is initialized and the ball is with an arbitrarily cup. In this case:
; a. “Ready...” is displayed on LCD;
; b. The cup LED with the ball is on, Other LEDs are off.

RESET:
		ldi r16, low(RAMEND)
		out SPL, r16
		ldi r16, high(RAMEND)
		out SPH, r16

		ser r16
		out DDRF, r16					; set Port F as OUTPUT, LCD Data    
		out DDRA, r16					; set Port A as OUTPUT, LCD Control    
		sts DDRL, r16					; set Port L as OUTPUT, LED Bar
		out DDRB, r16					; set Port B as OUTPUT, Result Indicator

		clr r16
		out DDRE, r16					; set Port E as INPUT, Control Motor  
		out PORTE, r16					; out 0 to PORTE
		    
		out PORTF, r16					; out 0 to PORTE
		out PORTA, r16					; out 0 to PORTA
		sts PORTL, r16					; out 0 to PORTL
		out PORTB, r16					; out 0 to PORTB

		cbi  DDRD,  0					; set PORTD pin0 to input
		sbi  PORTD, 0
		cbi  DDRD,  1					; set PORTD pin1 to input
		sbi  PORTD, 1

		ldi r16, PORTCDIR			    ; 0xF0 to r16
		out DDRC, r16			        ; columns are outputs, rows are inputs
		clr r17							; clear r17

		; LCD initialization
		do_lcd_command 0b00111000 		; 2x5x7
		rcall sleep_5ms

		do_lcd_command 0b00111000 		; 2x5x7
		rcall sleep_1ms

		do_lcd_command 0b00111000 		; 2x5x7
		do_lcd_command 0b00111000 		; 2x5x7

		do_lcd_command 0b00001000 		; display off
		do_lcd_command 0b00000001 		; clear display
		do_lcd_command 0b00000110 		; increment, no display shift
		do_lcd_command 0b00001100 		; Display on, Cursor off, no blink

DisplayReady:
		; set first line address		; for display Ready...
		do_lcd_command 0b10000000
		do_lcd_data 'R'
		do_lcd_data 'e' 
		do_lcd_data 'a'
		do_lcd_data 'd'
		do_lcd_data 'y'
		do_lcd_data '.'
		do_lcd_data '.'
		do_lcd_data '.'

		ldi r16, 0x20					; LCD bit0 对应 PORTL bit7, LCD bit1 对应 PORTL bit6...
		sts PORTL, r16					; write the pattern 0x20, an arbitrarily cup is on


; Step2: When the push button is pressed, the game starts and the ball is shuffled under the three cups.
; a. “Start ...” is displayed on LCD;
; b. Motor spins;
; c. Three cup LEDs are all on, but in dimmed light; other LEDs remain off.

Step2:
		sbic PIND, 0					; PIND bit0 for motor start spin
		rjmp Step2
		rjmp DisplayS

DisplayS:
		DisplayStart					; macro for LCD display Start...

MotorSpin:								; motor start spin
		ser r16
		out PORTE, r16
	
		; generate dimmedlight
		DimmedLight dim_light			; macro for dimmed light

P1:
		ldi ZL, 0x08					; write the pattern1
		sts PORTL, ZL					; output the pattern1
		TimeDelay						; delay
switch1:
		sbic PIND, 1					; check if that bit is clear ; if yes skip the next instruction
		rjmp P2							; rjmp to p2
		rjmp MotorStop					; rjmp to switch1
	
P2:
		ldi ZL, 0x10					; write the pattern2
		sts PORTL, ZL					; output the pattern2
		TimeDelay						; delay
switch2:
		sbic PIND, 1					; check if that bit is clear ; if yes skip the next instruction
		rjmp P3							; rjmp to p3
		rjmp MotorStop					; rjmp to switch2

P3:
		ldi ZL, 0x20					; write the pattern3
		sts PORTL, ZL					; output the pattern3
		TimeDelay						; delay
switch3:
		sbic PIND, 1					; check if that bit is clear ; if yes skip the next instruction
		rjmp P1							; rjmp to p1
		rjmp MotorStop					; rjmp to switch3


; Step3: 
; When the player wants to make a guess for the ball position 
; by pressing the push button again, the ball shuffle stops.
; a. The motor stops;
; b. The three cup LEDs remain dimmed;
; c. After the player keys in the ball position on the key pad, the cups are removed, 
;    the ball position is uncovered and the score is determined.

MotorStop:
		; ball shuffle stop
		sts PORTL, ZL					; After pressing push button again, the ball shuffle stops
				
		clr temp2
		out PORTE, temp2				; motor stop spin

		rjmp keypadmain
loop1:									; for jump to RESET
		jmp RESET

keypadmain:
		ldi cmask, INITCOLMASK			; initial column mask
		clr col							; initial column

colloop:
		cpi  col, 4						; compare column with 4
		breq keypadmain					; if equal, go to keypadmain	
		
continue: 
		out PORTC, cmask				; set column to mask value (one column off)
		ldi temp1, 0xFF

delay:
		dec  temp1						; decrease by 1
		brne delay

		in   temp1, PINC				; read PORTC
		andi temp1, ROWMASK				; Logical AND with Immediate
		cpi  temp1, 0x0F				; check if any rows are on
		breq nextcol					; branch to nextcol

		; delete dimmedlight											
		ldi LED_control, 0				; delete dimmedlight, if press button on the keypad, the cups are removed
		sts TCCR5B, LED_control	 
		sts TCCR5A, LED_control
										; if yes, find which row is on
		ldi rmask, INITROWMASK			; initialise row check
		clr row							; initial row

rowloop:
		cpi  row, 4						; compare r0w with 4
		breq nextcol
		mov  temp2, temp1
		and  temp2, rmask				; check masked bit
		breq convert					; if bit is clear, convert the bitcode
		
		inc row							; else move to the next row
		lsl rmask						; shift the mask to the next bit
		jmp rowloop

nextcol:
		lsl cmask						; else get new mask by shifting and 
		inc col							; increment column value
		jmp colloop						; and check the next column

		rjmp convert
loop2:									; for jump to loop1 than to RESET
		jmp loop1

convert:
		cpi col, 0						; compare clo with 0
		breq column0

		cpi col, 1						; compare clo with 1
		breq column1

		cpi col, 2						; compare clo with 2
		breq column2

		cpi col, 3						; compare clo with 3
		breq column3

column0:
		ldi temp1, 8					; load 8 to temp1
		jmp compare						; jump to compare

column1:
		ldi temp1, 16					; load 16 to temp1
		jmp compare						; jmp to compare

column2:
		ldi temp1, 32					; load 32 to temp1
		jmp compare						; jmp to compare

column3:
		nop								; else nop then jump to RESET

compare:
		; read PINL content
		lds temp, PINL					; load content in PINL to temp
		cp  temp, temp1					; compare contents in LED and Keypad
		breq scoreinc					; if equal, jump to scoreinc branch
		brne score0dec					; if not equal, jump to score0dec branch

loop3:									; for jump to loop2 then loop1 then RESET
		jmp loop2

score0dec:
		cpi  score, 0					; compare score with 0
		breq score0decdisplay			; if equal, jump to score0decdisplay branch
		brne scorenot0dec				; if not equal, jump to scorenot0dec branch

score0decdisplay:
		subi score, -'0'				; calcuate ASCII value
		do_lcd_command 0b00000001		; clear display
		do_lcd_score score				; display score on LCD
		TimeDelay
		jmp loop2

scorenot0dec:
		dec  score						; decrease by 1
		subi score, -'0'				; calcuate ASCII value for diaplay on LCD
		do_lcd_command 0b00000001		; clear display
		do_lcd_score score				; display score on LCD
		subi score, '0'					; change to number
		cpi score, 0					; compare score with 0
		TimeDelay						; delay
		breq loop3						; if score equal to 0, jump to RESET
		jmp SCANPIND					; jump to SCANPIND

scoreinc:
		inc score						; increase by 1
		FlashThreeTimes					; macro for flash few times
		subi score, -'0'				; calcuate ASCII value for diaplay on LCD
		do_lcd_command 0b00000001		; clear display
		do_lcd_score score				; display score
		subi score, '0'					; change to number
		jmp SCANPIND					; jump to SCANPIND

SCANPIND:
		sbic PIND, 0					; skip next instruction if PIND1 is cleared
		rjmp SCANPIND					; jump to SCANPIND
		jmp MotorSpin					; jump to MotorSpin


halt:
		rjmp halt

.equ LCD_RS = 7							; LCD control pin RS to PortA bit7
.equ LCD_RW = 5							; LCD control pin RW to PortA bit6
.equ LCD_E  = 6							; LCD control pin E to PortA bit5
.equ LCD_BE = 4							; LCD control pin BE to PortA bit4

.macro	lcd_set
		sbi PORTA, @0
.endmacro

.macro	lcd_clr
		cbi PORTA, @0
.endmacro


; Send a command to the LCD (r16)
lcd_command:							; for do LCD command macro use
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

.equ F_CPU = 16000000
.equ DELAY_1MS = F_CPU / 4 / 1000 - 4
; 4 cycles per iteration - setup/call-return overhead

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

