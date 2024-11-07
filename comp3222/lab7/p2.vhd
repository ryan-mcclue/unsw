-- TODO: what is blk_mem_gen_0?
-------------------------------------------------------------------------------
--
--  performs a binary search for the presence of a given value in a sorted ROM
--
-------------------------------------------------------------------------------
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;
USE ieee.std_logic_unsigned.all ;

-- index <= (low + (high - low)) // 2

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
        PORT( D, ResetD : IN STD_LOGIC_VECTOR(N-1 DOWNTO 0) ;
              E : IN STD_LOGIC ;
              Resetn : IN STD_LOGIC;
              Clock : IN STD_LOGIC ; 
              Q : OUT STD_LOGIC_VECTOR(N-1 DOWNTO 0) ) ;
    END COMPONENT;
	
    -- any other components
    SIGNAL low_reg: STD_LOGIC_VECTOR(4 DOWNTO 0);
    SIGNAL high_reg: STD_LOGIC_VECTOR(4 DOWNTO 0);
    CONSTANT low_reg_reset : INTEGER = 0;
    CONSTANT high_reg_reset : INTEGER = 31;
	
    TYPE State_type IS (Init, MemoryRequest, DataInspect, Finish); -- your states
    SIGNAL y, y_next : State_type ;
	
    SIGNAL address : STD_LOGIC_VECTOR(4 DOWNTO 0);
    SIGNAL data_out : STD_LOGIC_VECTOR(7 DOWNTO 0);
    -- any other signals

    SIGNAL index_bus : STD_LOGIC_VECTOR(7 DOWNTO 0);
    SIGNAL index_enables : STD_LOGIC_VECTOR(1 DOWNTO 0);
    SIGNAL index_resets : STD_LOGIC_VECTOR(1 DOWNTO 0);

BEGIN
    -- your code
    lowreg: regne PORT MAP (index_bus, low_reg_reset, index_enables(0), index_resets(0), Clock, low_reg);
    highreg: regne PORT MAP (index_bus, high_reg_reset, index_enables(1), index_resets(1), Clock, high_reg);

    muxes: WITH index_enables SELECT
      index_bus <= address - 1 WHEN "10", -- high
                  address + 1 WHEN "01", -- low
                  "000000000" WHEN OTHERS;

    addresscalc: PROCESS(low_reg, high_reg)
    BEGIN
      address <= (low_reg + (high_reg - low_reg)) >> 1;
    END PROCESS;

    -- IMPORTANT: use combinatorial blocks for circuit 
    -- IMPORTANT: only enables with states    
    statetable: PROCESS(y, s)
    BEGIN
        CASE y IS
            WHEN Init =>
                IF (s = '1') THEN
                    y_next <= MemoryRequest; 
                END IF; 
            WHEN MemoryRequest =>
              y_next <= DataCompare;
            WHEN DataCompare =>
              IF (data_out = Data)
                y_next <= Finished;
              ELSIF (high_reg > low_reg)
                y_next <= Finished;  
              ELSE
                y_next <= MemoryRequest;
              END IF;
        END CASE;
    END PROCESS;

    controlsignals: PROCESS(y, data_out, data)
    BEGIN
       -- Clear all outputs
       Done <= '0'; 
       Found <= '0'; 
       index_enables <= "00";
       index_resets <= "11";

       CASE y IS
          WHEN Init =>
            index_resets <= "00";
          WHEN MemoryRequest =>
          WHEN DataCompare =>
             IF (data_out < Data)
               index_enables(0) <= '1';
             ELSIF (data_out > Data)
               index_enables(1) <= '1';
             END IF;
          WHEN Finished =>
            Done <= '1';
            IF (data_out = Data) THEN
              Found <= '1';
            END IF;
       END CASE;
    END PROCESS;


    fsmflipflops: PROCESS(Clock, Resetn)
    BEGIN
      IF (Resetn = '0') THEN
        y <= Init;
      ELSIF (Clock'event AND Clock = '1') THEN
        y <= y_next;
      END IF;
    END PROCESS;

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
    PORT( D, ResetD : IN STD_LOGIC_VECTOR(N-1 DOWNTO 0) ;
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
            Q <= ResetD;
        ELSIF (E = '1') THEN
            Q <= D;
        END IF ;
    END PROCESS ;
END Behavior ;
