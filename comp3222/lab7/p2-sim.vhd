-------------------------------------------------------------------------------
--
-- presents all possible test vectors to perform binary searches for values in 
-- a 32-entry sorted ROM
--
-------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;

entity testbench is
end entity testbench;

architecture test_l7p2 of testbench is
    COMPONENT l7p2 IS
    PORT( Clock, Resetn : IN STD_LOGIC ;
          s : IN STD_LOGIC ;
          Data : IN STD_LOGIC_VECTOR(7 DOWNTO 0) ;
          Addr : OUT STD_LOGIC_VECTOR(4 DOWNTO 0) ;
          Found : OUT STD_LOGIC ;
          Done : OUT STD_LOGIC ) ;
    END COMPONENT;
    SIGNAL value : std_logic_vector(7 DOWNTO 0);
    SIGNAL address : std_logic_vector(4 DOWNTO 0);
    SIGNAL clk, Resetn, s, Found, Done, increment : std_logic; 
    constant ClockPeriod : TIME := 10 ns;
begin

    UUT : l7p2 port map (clk, Resetn, s, value, address, Found, Done);

    clck: process begin
        clk <= '0';
	     wait for 100 ns;    -- wait for global reset after device powers up
        loop
             wait for (ClockPeriod / 2); 
             clk <= not clk;
        end loop;
    end process clck;

    cntr: process (Resetn, clk) 
    begin
        IF Resetn = '0' THEN
            value <= (OTHERS => '0');
        ELSIF clk'event AND clk = '1' THEN
            IF increment = '1' THEN
                value <= value + '1';
            END IF;
        END IF;
    END PROCESS;

    stimulus: process begin
       Resetn <= '0'; increment <= '0'; s <= '0';
	
       wait for 140 ns;    -- wait for global reset after device powers up
         Resetn <= '1';    -- deassert reset
       wait for 20ns;
         s <= '1';

       for i in 0 to 64 loop
         wait for 500ns;
           s <= '0';
         wait for 10ns;
           increment <= '1';
         wait for 10ns;
           increment <= '0';
         wait for 10ns;
           s <= '1';
       end loop;

       wait for 500ns;
         s <= '0';
       wait;
         
    end process stimulus;

end architecture test_l7p2;
