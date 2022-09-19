<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Addition will yield a sum (XOR) and a carry (AND) bit.
So, generalising to multiple bits, moving along a number the carry output bit
becomes the carry input bit for the next

Checkable pattern in Karnaugh map indicates odd function (i.e. indice is odd)

Full-adder can be represented as two half-adders in series
Ripple carry adder is combination of full adders

Whenever carry-out with twos complement just ignore. (for ones complement, have to add back in)

An adder/subtractor unit will have a control line set to 1 when subtracting.
This 1 toggles all the bits and is added again to convert to twos complement

Critical path delay is longest delay

n-wide 2-1 multiplexor.

Faster addition is carry-lookahead
All carries produced after 3-gate delays
All sum bits after 4-gate delays
* These delays differ if using a ripple-carry between blocks or hierarchical
(fan-in constraints determine which to use?)
* On our FPGAs below 64bit, ripple-carry faster than carry-lookahead?

Overflow determined by (MSB-carry-in XOR carry-out)

* As calculation of sum and carry bit have different propagation delays, 
take some time for output to be valid. require clock?
(will be seen as 'glitching' in waveform simulator)
