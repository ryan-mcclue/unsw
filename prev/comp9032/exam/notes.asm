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

; GPIO output (led)
  ser r16
  STORE DDRC, r16
  STORE PORTC, r16

; GPIO input (button)
  clr r16
  STORE DDRD, r16
  STORE PORTD, r16
  sbic PIND, 0

; Keypad

; Stack pointer
  ldi r16, low(RAMEND)
  out SPL, r16
  ldi r16, high(RAMEND)
  out SPH, r16

  push YL
  push YH

  in YL, SPL
  in YH, SPH
  sbiw YH:YL, 8
  out SPL, YL
  out SPH, YH

  st Y+1, r16

  pop YH
  pop YL

  adiw YH:YL, 8
  out SPH, YH
  out SPL, YL
    

; Button interrupt
.org INT0addr
  jmp pb0_press

  ldi r16, (2 << ISC00); set INT0~PB0 as falling edge triggered interrupt
  sts EICRA, r16
  in r16, EIMSK
  ori r16, (1 << INT0); enable INT0~PB0
  out EIMSK, r16

pb0_press:
  push r16
  in r16, SREG
  
  pop r16
  out r16, SREG 
  reti

; Timer interrupt
.org OVF0addr
  jmp update_loop

  ldi r16, 0x00; Set-up Timer0 Overflow, 8 bits counter, no output compare
  out TCCR0A, r16
  ldi r16, (1<<CS00) | (1<<CS02) ;prescaling value=1024, 256*1024/16Mhz=16ms, thus, TIMER_TICK_COUNT_1S = 62
  out TCCR0B, r16
  ldi r16, 1<<TOIE0; enable the Overflow Interrupt
  sts TIMSK0, r16; T/C0 interrupt enable
  reti

reset:
  sei
