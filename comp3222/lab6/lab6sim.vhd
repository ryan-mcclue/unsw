-------------------------------------------------------------------------------
--
-- testbench provides stimuli to processor from l6p1
--
-------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;

entity testbench is
end entity testbench;

architecture test_l6p1 of testbench is
    COMPONENT l6p1sim IS
	PORT( DIN : IN std_logic_vector(8 DOWNTO 0);
	      Resetn, Clock, Run : IN std_logic;
              Done : BUFFER std_logic;
	      BusWires : BUFFER std_logic_vector(8 DOWNTO 0));
    END COMPONENT;
    SIGNAL DIN, BusWires : std_logic_vector(8 DOWNTO 0);
    SIGNAL clk, Resetn, Run, Done : std_logic; 
    constant ClockPeriod : TIME := 20 ns;
begin

    UUT : l6p1sim port map (DIN, Resetn, clk, Run, Done, BusWires);

    clck: process begin
        clk <= '0';
	     wait for 100 ns;    -- wait for global reset after device powers up
        loop
             wait for (ClockPeriod / 2); 
             clk <= not clk;
        end loop;
    end process clck;

    stimulus: process begin
	
       wait for 120 ns;    -- wait for global reset after device powers up
         Resetn <= '0';    -- assert active low reset 
         Run <= '0';
         DIN <= (OTHERS => '0');
       wait for 20 ns;
         Resetn <= '1';    -- deassert reset
       -- add your stimuli here
         Run <= '1';
         -- DIN, IR octal
         -- BusWires hex
         DIN <= 8#100#;
       -- IMPORTANT: may have to do before clock edge
       wait for ClockPeriod;
         DIN <= 8#005#; 
         Run <= '0';
       wait for ClockPeriod;
         Run <= '1'
         DIN <= 8#010#; 
       wait for ClockPeriod;
         Run <= '0';
       wait for ClockPeriod;
         Run <= '1';
         DIN <= 8#201#; 
       wait for ClockPeriod;
         Run <= '0';
       wait for (3 * ClockPeriod);
         Run <= '1';
         DIN <= 8#300#; 
       wait for ClockPeriod;
         Run <= '0';
       wait;
         
    end process stimulus;

end architecture test_l6p1;
