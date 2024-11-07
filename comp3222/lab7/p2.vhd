-- TODO: what is blk_mem_gen_0?

-------------------------------------------------------------------------------
--
--  performs a binary search for the presence of a given value in a sorted ROM
--
-------------------------------------------------------------------------------
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;
USE ieee.std_logic_unsigned.all ;

bin(data)
SIGNAL low, index : STD_LOGIC_VECTOR(4 DOWNTO 0);
SIGNAL high : STD_LOGIC_VECTOR(4 DOWNTO 0) := "01111"; -- len(32) - 1

-- TODO: why does example code have 'labels:' for processes? 

-- index <= (low + (high - low)) // 2
-- TODO: can use right_shift() function or have to use shift register?

  
states:
  addr_calc:
    if s = '1'
      data_request
  data_request:
    data_inspect
  data_inspect:
    -- TODO: how to capture 3 chain if else in ASM conditional block? (chain conditional blocks)
    -- TODO: how to show different outputs on state box
    if dout == val or high < low:
      done
    else if dout > val:
      update_high
    else:
      update_low
  update_high:
  update_low:
    addr_calc;
  done:
     
  reg(high_enable, addr + 1, addr - 1
  reg

outputs:
  addr_calc:
    addr <= (low + (high - low)) >> 1
    load_wide into shift
    shift
  data_request:
    -- just want clock cycle for memory block latency
  data_inspect:
    -- just transitions
  update_high:
      high_enable <= '1' high <= addr - 1;
      high <= addr - 1 WHEN high_enable ELSE high;
  update_low:
      -- we will need a register if want value to persist across clock cycles
      -- TODO: clarify why can't do this (sensitivity list?)
      low <= addr + 1;
  done:
    done <= '1';
    if dout == val:
      found <= '1';
    elif high < low:
      found <= '0';


    high reg (high_enable, bus_wires);
    low reg (low_enable_ bus_wires)

    addr_sum <= (low + (high - low));
    
    addr shiftreg(addr_enable, addr_sum);
    
    next_high <= addr - 1;
    next_low <= addr + 1;
    muxes: WITH search_higher SELECT
        bus_wires <= next_high WHEN "1",
                    next_low WHEN OTHERS;


ENTITY l7p2 IS
    PORT( Clock, Resetn : IN STD_LOGIC ;
          s : IN STD_LOGIC ;
          Data : IN STD_LOGIC_VECTOR(7 DOWNTO 0) ;
          Addr : OUT STD_LOGIC_VECTOR(4 DOWNTO 0) ;
          Found : OUT STD_LOGIC ;
          Done : OUT STD_LOGIC ) ;
END l7p2 ;

ARCHITECTURE Behavior OF l7p2 IS
    COMPONENT blk_mem_gen_0 IS
        PORT ( clka : IN STD_LOGIC;
               addra : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
               douta : OUT STD_LOGIC_VECTOR(7 DOWNTO 0));
    END COMPONENT;
    COMPONENT regne IS
        GENERIC ( N : INTEGER := 8 ) ;
        PORT( D : IN STD_LOGIC_VECTOR(N-1 DOWNTO 0) ;
              E : IN STD_LOGIC ;
              Resetn : IN STD_LOGIC;
              Clock : IN STD_LOGIC ; 
              Q : OUT STD_LOGIC_VECTOR(N-1 DOWNTO 0) ) ;
    END COMPONENT;
	
    -- any other components
	
    TYPE State_type IS ( ); -- your states
    SIGNAL y, y_next : State_type ;
	
    SIGNAL address : STD_LOGIC_VECTOR(4 DOWNTO 0);
    SIGNAL data_out : STD_LOGIC_VECTOR(7 DOWNTO 0);
    
    -- any other signals

BEGIN

    -- your code
	
    mem_blk: blk_mem_gen_0
        PORT MAP ( clka => Clock,
                   addra => address,
                   douta => data_out );

END Behavior ;

LIBRARY ieee ;
USE ieee.std_logic_1164.all ;

-- n-bit register with synchronous reset and enable
ENTITY regne IS
    GENERIC ( N : INTEGER := 8 ) ;
    PORT( D : IN STD_LOGIC_VECTOR(N-1 DOWNTO 0) ;
          E : IN STD_LOGIC ;
          Resetn : IN STD_LOGIC;
          Clock : IN STD_LOGIC ;
          Q : OUT STD_LOGIC_VECTOR(N-1 DOWNTO 0) ) ;
END regne ;

ARCHITECTURE Behavior OF regne IS
BEGIN
    PROCESS
    BEGIN
        WAIT UNTIL (Clock'EVENT AND Clock = '1') ;
        IF (Resetn = '0') THEN
            Q <= (OTHERS => '0');
        ELSIF (E = '1') THEN
            Q <= D;
        END IF ;
    END PROCESS ;
END Behavior ;
