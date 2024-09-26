<!-- SPDX-License-Identifier: zlib-acknowledgement -->
half adder adds two bits
```
s <= x XOR y;
cout <= x AND y;
```

full adder (chained half-adders) adds two bits and carry
```
s <= x XOR y XOR cin;
cout <= (x AND y) OR (cin AND x) OR (cin AND y);
```

gate delay means there is settling time for output.
a clock can remove this effect

n-bit ripple carry adder (chained full-adders) 
IMPORTANT: lsb carry to msb
```
entity adder4 is
  port (cin: in std_logic;
        x: in std_logic_vector(3 downto 0);
        y: in std_logic_vector(3 downto 0);
        s: out std_logic_vector(3 downto 0);
        cout: out std_logic);
end adder4;

-- entity and arch of fulladd before this in file
package fulladd_package is
  component fulladd
    port (cin, x, y: in std_logic;
          s, cout: out std_logic); 
  end component;
end fulladd_package;

use work.fulladd_package.all;
architecture behaviour of adder4 is
  signal c: std_logic_vector(2 downto 0);

  A0: fulladd port map (cin, x(0), y(0), s(0), c(0));
  A1: fulladd port map (c(0), x(1), y(1), s(1), c(1));
  A2: fulladd port map (c(1), x(2), y(2), s(2), c(2));
  A3: fulladd port map (c(3), x(3), y(3), s(3), cout);
end behaviour;
```

twos-complement used as easier overflow detection, 
same circuit for subtraction/addition and
compatibility with signed and unsigned
in twos complement, if the carry-out of the MSB/sign-bit is different
to the carry-in of the previous bit then overflow 

carry lookahead adder reduces critical path delay of carries in ripple-carry
it will first determine if inputs will generate (both 1s) or 
propagate a carry (either 1 and carry in)
once all carries determined, full adder components occur in parallel

as CLA complex with more wires, often divide into 8bit chunks and connect with ripple
this is known as hierachical carry-lookahead addition

TODO: look at the timing simulation of LPM adder (using '+' operator) 
to observe glitching as carries ripple through adder

```
Sum <= ('0' & X) + (‘0’ & Y) + Cin ;
S <= Sum(15 DOWNTO 0) ;
Cout <= Sum(16) ;
Overflow <= Sum(16) XOR X(15) XOR Y(15) XOR Sum(15) ;
```

cross-bar switch has capability of connecting any of its inputs to any
of its outputs.
in this way, multiplexors can be thought of as lookup tables.
a 2x2 crossbar switch can be built with two multiplexors.
by rewriting a truth table's outputs to include say a variable,
resulting circuit can be more efficient

muxes can implement a variety of logic functions like xor, majority function

can simplify truth tables if group values to say x, e.g. where x is all 1 and 0.
then see how output relates to remaining variable, e.g. y

shannon's expansion theorem can map truth table to mux:
  1. factor out a variable in normal and uncomplemented
     the factored out variable becomes a control signal
  2. continue factoring inside brackets for desired data lines
     the inner most variables become data lines

(cofactors are subfunctions?)


decoder converts binary code to one-hot encoded output (i.e. unique 1 bit set like bit mask)
so, n inputs, 2^n outputs
has enable pin so can control having no output
used in memory address decoding and demultiplexing
so 2-4, 3-8 decoders etc.

tristate buffer has option of being in high-impedance (imagine no wires are disconnected, i.e. air between them)
this allows sharing of bus/line

encoder converts one-hot encoded input to binary code
4-2, 8-3 encoders etc.
priority encoder allows more than 1 bit to be active.
in this case, will select binary code for highest priority bit (typically from MSB)
used in interrupt handlers

TODO: combinational vhdl code for these components



karnaugh map generator:
http://www.32x8.com/index.html
