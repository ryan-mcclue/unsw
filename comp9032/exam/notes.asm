; Address spaces
.macro STORE
	.if @0 > 0x40
		sts @0, @1
	.else
		out @0, @1
	.endif
.endmacro

.macro LOAD
	.if @1 > 0x40
		lds @0, @1
	.else
		in @0, @1
	.endif
.endmacro

; Reading
	ldi r31, HIGH(@2)
	ldi r30, LOW(@2)
	ld @0, z+
	ld @1, z

; Writing
	ldi r31, HIGH(@2)
	ldi r30, LOW(@2)
	st z+, @0
  st z, @1

; Program Memory
.cseg
str: db "ryan", 0
	mov zl, low(str)
	mov zh, high(str)
	lpm r16, z+
	cpi r16, 0

; Data Memory
.dseg
var: .byte 1

; Unsigned 
brsh, brlo, brcs

; Signed
brge, brlt, brvs

; Multibyte
adc, sbc, cpc


; GPIO input/output

; Keypad, ...

; PWM

; Stack pointer
	ldi r16, low(RAMEND)
	out SPL, r16
	ldi r16, high(RAMEND)
	out SPH, r16

; Button interrupt
.org INT0addr
  jmp eastentry_button_press

; Timer interrupt
.org OVF0addr
  jmp update_loop

reset:
  sei
