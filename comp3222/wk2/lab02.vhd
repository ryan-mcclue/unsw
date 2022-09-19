LIBRARY ieee;
USE ieee.std_logic_1164.all;

-- TODO(Ryan): Different names for combining two 2-1 muxes to form 3-1 and
-- vertically combining 2-1 muxes to form n-wide 2-1 mux?

-- TODO(Ryan): 2-1 mux with signal 0 = X
-- output <= (NOT(signal) AND x) OR (signal AND y);
-- PROCEDURE mux_2to1() IS
-- BEGIN
-- END mux_2to1

-- TODO(Ryan): Is there a way to not have to specify specific pin assignments here?
-- e.g. keep X and Y and then make pin assignment in architecture 
ENTITY lab01_2 IS
  PORT (SW: IN STD_LOGIC_VECTOR(9 DOWNTO 0);
        LEDG: OUT STD_LOGIC_VECTOR(3 DOWNTO 0));
END lab01_2;

-- NOTE(Ryan): SW(9) = S, SW(3,0) = X, SW(7,4) = Y, LEDG(3,0) = M
ARCHITECTURE mux_4wide_2to1 OF lab01_2 IS
BEGIN
  LEDG(0) <= (NOT(SW(9)) AND SW(0)) OR (SW(9) AND SW(4));
  LEDG(1) <= (NOT(SW(9)) AND SW(1)) OR (SW(9) AND SW(5));
  LEDG(2) <= (NOT(SW(9)) AND SW(2)) OR (SW(9) AND SW(6));
  LEDG(3) <= (NOT(SW(9)) AND SW(3)) OR (SW(9) AND SW(7));
END mux_4wide_2to1;


ARCHITECTURE mux_2wide_3to1 OF lab01_3 IS
  SIGNAL mux1_o, mux2_o: STD_LOGIC; 
BEGIN
  mux1_o <= (NOT(SW(9)) AND SW(0)) OR (SW(9) AND SW(1));
  LEDG(0) <= (NOT(SW(8)) AND mux1_o) OR (SW(8) AND SW(2));

  mux2_o <= (NOT(SW(9)) AND SW(3)) OR (SW(9) AND SW(4));
  LEDG(1) <= (NOT(SW(8)) AND mux2_o) OR (SW(8) AND SW(5));
END mux_2wide_3to1;

-- 00 = d(6,4,3,2,1), 01 = E(0,6,3,5,4), 10 = 1(1,2), 11 = blank (all 1's)

