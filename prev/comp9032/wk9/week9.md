<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Parallel interface more expensive with more wires 
(also, for long distance more wires increases susceptibility to noise)

At reciever transmitter side, will convert the parallel signal from MCU into serial.
Conversely, reciever will convert serial to parallel
(so all serial ports implement a parallel-in-serial-out-shift-register?)

synchronous requires extra hardware to synchronise clocks to allow faster data rate
asynchronous more common 
UART is hardware:
  * 'mark' level is logic 1 (when idle, holds this level)
  * 'space' level is logic 0
  *  start bit (change from mark to space level), stop bit
  *  baud rate, bps

Connection types:
  * simplex (one-way only)
  * half-duplex (one-way at a time)
  * full-duplex (each way same time)

Devices:
  * DCM (data communications equipment), 
    e.g. modem (modulator/demodulator, typically converts for use over telephone line)
  * DTE (data terminal equipment), e.g. PC

RS-232-C common serial standard (defining handshake, data direction flow, signal levels, etc.)
