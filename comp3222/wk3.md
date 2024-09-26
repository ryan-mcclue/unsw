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

TODO: 1 to 3 for nonnumeric signals?
TODO: twos-complement subtraction and addition
      can use same circuit with xor select?

carry lookahead adder reduces critical path delay of carries
it will first determine if inputs will generate (both 1s) or 
propagate a carry (either 1 and carry in)
once all carries determined, full adder components occur in parallel
as CLA complex with more wires, often divide into 8bit chunks and connect with ripple
this is known as hierachical carry-lookahead addition
TODO: detecting overflow by looking at MSB?

TODO: look at the timing simulation of LPM adder (using '+' operator) 
to observe glitching as carries ripple through adder

TODO: want to be able to access internal signals of say '+' operator to see if overflow?

```
Sum <= ('0' & X) + (‘0’ & Y) + Cin ;
S <= Sum(15 DOWNTO 0) ;
Cout <= Sum(16) ;
Overflow <= Sum(16) XOR X(15) XOR Y(15) XOR Sum(15) ;
```

cross-bar switch connects n inputs to k outputs (built with multiplexors)
muxes can create xor, majority function

TODO: shannon's expansion theorem to create functions with muxes
TODO: decoder circuits

karnaugh map generator:
http://www.32x8.com/index.html


