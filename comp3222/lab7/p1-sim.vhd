-------------------------------------------------------------------------------
--
-- provides stimulus to the popcount function of Lab 7 Part I
-- requires extension by the student completing the lab exercise
--
-------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;

entity testbench is
end entity testbench;

architecture test_l7p1 of testbench is
    COMPONENT l7p1sim IS
	    PORT( ... ) ;
    END COMPONENT;
    SIGNAL ...;
    constant ClockPeriod : TIME := 10 ns;
begin

    UUT : l7p1sim port map ( ... );

    clck: process begin
        clk <= '0';
	     wait for 100 ns;    -- wait for global reset after device powers up
        loop
             wait for (ClockPeriod / 2); 
             clk <= not clk;
        end loop;
    end process clck;

    stimulus: process begin
      
      -- Test, 0000, 1111, 1010, altering 's' signal
      -- TODO: What are some corner cases?
	
       wait for 120 ns;    -- wait for global reset after device powers up
         Resetn <= '0';    -- assert active low reset 
       wait for 10 ns;
         Resetn <= '1';    -- deassert reset
         ...
       wait for 10ns;
         ...
       wait;
         
    end process stimulus;

end architecture test_l7p1;

