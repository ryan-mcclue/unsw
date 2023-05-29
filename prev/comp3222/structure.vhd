LIBRARY ieee;
USE ieee.std_logic_1164.all;

ENTITY main_entity IS
  PORT (SW: IN STD_LOGIC_VECTOR(9 DOWNTO 0);
        HEX0, HEX1, HEX2, HEX3: OUT STD_LOGIC_VECTOR(7 DOWNTO 0));
END main_entity

ARCHITECTURE main_architecture OF main_entity IS
  -- Place this in a PACKAGE
  -- do we also define ARCHITECTURE in PACKAGE?
  COMPONENT some_func
    PORT (X, Y: IN STD_LOGIC;
          Z: OUT STD_LOGIC);
  END COMPONENT
  SIGNAL scratch: STD_LOGIC;
BEGIN
  some_func0: some_func PORT MAP (SW(9), SW(8), HEX0(1));
END main_architecture

ENTITY some_func IS
    PORT (X, Y: IN STD_LOGIC;
          Z: OUT STD_LOGIC);
END some_func;

ARCHITECTURE some_func_arch OF some_func IS
END some_func_arch;
