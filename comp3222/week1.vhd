LIBRARY ieee;
USE ieee.std_logic_1164.all; -- STD_LOGIC: Z (high impedance just open circuit?)

ENTITY func1 IS
  PORT (x1, x2, x3: IN BIT;
        f: OUT BIT);
END func1;

ARCHITECTURE logic_func OF func1 IS
BEGIN
  f <= (NOT x1 AND x2) OR
       (NOT x3 AND x1);
END logic_func;
