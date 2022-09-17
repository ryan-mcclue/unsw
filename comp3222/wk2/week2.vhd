LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.std_logic_signed.all; -- gives use synthesisable operators +, -, *

-- Library of Parameterised Modules


ENTITY full_adder IS
  PORT (c_in, x, y: IN STD_LOGIC;
        sum, c_out: OUT STD_LOGIC);
END full_adder;

ARCHITECTURE logic_func OF full_adder IS
BEGIN
  sum <= x XOR y XOR c_in;
  c_out <= (x AND y) OR (c_in AND x) OR (c_in AND y);
END logic_func;

-------------------------------------------------------

ARCHITECTURE structure OF adder4 IS
  -- these can be thought of as private connections/wires not present in interface
  SIGNAL c1, c2, c3: STD_LOGIC; 
  COMPONENT full_adder
    PORT (c_in, x, y: IN STD_LOGIC;
          sum, c_out: OUT STD_LOGIC);
  END COMPONENT;
BEGIN
  stage0: full_adder -- instantiating a copy of full_adder
    PORT MAP (); -- pass arguments to component
END structure;

-- USE work.full_adder_package.all (working directory; all sub components)
PACKAGE full_adder_package IS
  COMPONENT full_adder
    PORT (c_in, x, y: IN STD_LOGIC;
          sum, c_out: OUT STD_LOGIC);
  END COMPONENT;
END full_adder_package;

--------------------------------------------------
ENTITY adder4 IS
PORT ( Cin : IN STD_LOGIC ;
X, Y : IN STD_LOGIC_VECTOR(3 DOWNTO 0) ; -- think of as X is a 4 bit value
S : OUT STD_LOGIC_VECTOR(3 DOWNTO 0) ; -- numeric signals
Cout : OUT STD_LOGIC ) ;
END adder4 ;

ARCHITECTURE Structure OF adder4 IS
SIGNAL C : STD_LOGIC_VECTOR(1 TO 3) ; -- unrelated signals
BEGIN
stage0: fulladd PORT MAP ( Cin, X(0), Y(0), S(0), C(1) ) ;
stage1: fulladd PORT MAP ( C(1), X(1), Y(1), S(1), C(2) ) ;
stage2: fulladd PORT MAP ( C(2), X(2), Y(2), S(2), C(3) ) ;
stage3: fulladd PORT MAP ( C(3), X(3), Y(3), S(3), Cout ) ;
END Structure 

------ 
ENTITY adder16 IS
PORT ( Cin : IN STD_LOGIC ;
X, Y : IN STD_LOGIC_VECTOR(15 DOWNTO 0) ;
S : OUT STD_LOGIC_VECTOR(15 DOWNTO 0) ;
Cout, Overflow : OUT STD_LOGIC ) ;
END adder16 ;

ARCHITECTURE Behavior OF adder16 IS
SIGNAL Sum : STD_LOGIC_VECTOR(16 DOWNTO 0) ;
BEGIN
Sum <= ('0' & X) + (‘0’ & Y) + Cin ; -- concatenation '&' adds a 0 bit
S <= Sum(15 DOWNTO 0) ;
Cout <= Sum(16) ;
Overflow <= Sum(16) XOR X(15) XOR Y(15) XOR Sum(15) ; -- LPM does not give overflow automatically?
END Behavior ;

------
ENTITY adder16 IS
PORT ( X, Y : IN INTEGER RANGE -32768 TO 32767 ;
S : OUT INTEGER RANGE -32768 TO 32767 ) ;
END adder16 ;

ARCHITECTURE Behavior OF adder16 IS
BEGIN
S <= X + Y ;
END Behavior ;
