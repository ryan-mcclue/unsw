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
    COMPONENT l7p1 IS
	    PORT( Clock, Resetn	: IN STD_LOGIC;
              s	: IN STD_LOGIC;
              Data : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
              B : BUFFER STD_LOGIC_VECTOR(3 DOWNTO 0);
              Done : OUT STD_LOGIC );
    END COMPONENT;
    
    SIGNAL clk, resetn, s, done : STD_LOGIC;
    SIGNAL data: STD_LOGIC_VECTOR(7 DOWNTO 0);
    SIGNAL b: STD_LOGIC_VECTOR(3 DOWNTO 0);
    
    -- TODO: changed from 10ns to 20ns as to match previous lab?
    constant ClockPeriod : TIME := 20 ns;
begin

    UUT : l7p1 port map (clk, resetn, s, data, b, done);

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
         resetn <= '0';    -- assert active low reset 
       wait for ClockPeriod;
         resetn <= '1';    -- deassert reset
         
         -- load 00111011 into A
         data <= "00111011";
         s <= '0';
       wait for ClockPeriod; 
         -- clear data and begin
         data <= "00000000";
         s <= '1';
       wait for ClockPeriod * 10;
       
         -- load 11111111 into A
         data <= "11111111";
         s <= '0';
         -- wait for two cycles to transition to S1 and then load
       wait for ClockPeriod * 2; 
         -- clear data and begin
         data <= "00000000";
         s <= '1';
        wait for ClockPeriod * 10;
         
         -- load 00000000 into A
         data <= "00000000";
         s <= '0';
         -- wait for two cycles to transition to S1 and then load
       wait for ClockPeriod * 2; 
         -- begin
         s <= '1';
        wait for ClockPeriod * 5;
        
         -- load 00110100 into A
         data <= "00110100";
         s <= '0';
         -- wait for two cycles to transition to S1 and then load
       wait for ClockPeriod * 2;
         -- clear data and begin
         data <= "00000000";
         s <= '1';
       wait for ClockPeriod * 2;
         -- ensure reset goes to S1
         resetn <= '0';
         
       wait;
         
    end process stimulus;

end architecture test_l7p1;



-------------------------------------------------------------------------------
--
-- provides stimulus to the popcount function of Lab 7 Part I
-- requires extension by the student completing the lab exercise
--
-------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;

-- TODO: have to right-click (set as top) on testbench file to not have undefined
-- TODO: rename component name to l7p1 (i.e. remove sim ending) 
-- TODO: add 's' to sensitivity list to FSM_outputs 

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

