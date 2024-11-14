-------------------------------------------------------------------------------
--
--  performs a binary search for the presence of a given value in a sorted ROM
--
-------------------------------------------------------------------------------
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;
USE ieee.std_logic_unsigned.all ;

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
        GENERIC ( N : INTEGER := 5 ) ;
        PORT( D : IN STD_LOGIC_VECTOR(N-1 DOWNTO 0) ;
              E : IN STD_LOGIC ;
              Resetn : IN STD_LOGIC;
              Clock : IN STD_LOGIC ; 
              Q : OUT STD_LOGIC_VECTOR(N-1 DOWNTO 0) ) ;
    END COMPONENT;

    -- any other components
	
    -- any other signals
    TYPE State_type IS (InitLow, InitHigh, MemoryRequest, DataStore, DataInspect, Finish); -- your states
    SIGNAL y, y_next : State_type ;
	
    SIGNAL address : STD_LOGIC_VECTOR(5 DOWNTO 0);
    SIGNAL data_out : STD_LOGIC_VECTOR(7 DOWNTO 0);

    SIGNAL data_reg: STD_LOGIC_VECTOR(7 DOWNTO 0);
    SIGNAL data_enable: STD_LOGIC;

    SIGNAL buss : STD_LOGIC_VECTOR(5 DOWNTO 0);
    SIGNAL enables : STD_LOGIC_VECTOR(1 DOWNTO 0);

    SIGNAL low_reg: STD_LOGIC_VECTOR(5 DOWNTO 0);
    SIGNAL high_reg: STD_LOGIC_VECTOR(5 DOWNTO 0);
    SIGNAL address_shift : STD_LOGIC_VECTOR(5 DOWNTO 0);
    
    SIGNAL init: STD_LOGIC;
    SIGNAL low: STD_LOGIC;
BEGIN
    low <= '1';
    -- your code
    lowreg: regne GENERIC MAP (n => 6) PORT MAP (buss, enables(0), low, Clock, low_reg);
    highreg: regne GENERIC MAP (n => 6) PORT MAP (buss, enables(1), low, Clock, high_reg);
    datareg: regne GENERIC MAP (n => 8) PORT MAP (data_out, data_enable, low, Clock, data_reg);
    
    addresscalc: PROCESS(low_reg, high_reg, address_shift)
    BEGIN
      -- do calculation in 6bits to account for overflow in 5bits, e.g. when high + low >= 32 >= 2^5
      address_shift <= (high_reg + low_reg);
      address <= "0" & address_shift(5 DOWNTO 1);

      Addr <= address(4 DOWNTO 0);
    END PROCESS;
	
    mem_blk: blk_mem_gen_0 PORT MAP (clka => Clock, addra => address(4 DOWNTO 0), douta => data_out);
    
    muxes: WITH enables & init SELECT
      buss <= "011111" WHEN "101", -- high, init (set to 31)
              "000000" WHEN "011", -- low, init (set to 0)
              address - 1 WHEN "100", -- high
              address + 1 WHEN "010", -- low,
              "000000" WHEN OTHERS;
                  
    statetable: PROCESS(y, s, data_reg, high_reg, low_reg, Data)
    BEGIN
        CASE y IS
            WHEN InitLow =>
                y_next <= InitHigh;
            WHEN InitHigh =>
                IF (s = '1') THEN
                    y_next <= MemoryRequest; 
                END IF; 
            WHEN MemoryRequest =>
              y_next <= DataStore;
            WHEN DataStore =>
              -- store in register to account for any weird IP memory block changes
              y_next <= DataInspect;
            WHEN DataInspect =>
              IF (data_reg = Data OR low_reg >= high_reg) THEN
                y_next <= Finish;
              ELSE
                y_next <= MemoryRequest;
              END IF;
            WHEN Finish =>
              IF (s = '0') THEN
                y_next <= InitLow;
              END IF;
        END CASE;
    END PROCESS;

    controlsignals: PROCESS(y, data_reg, Data)
    BEGIN
       -- Clear all outputs
       Done <= '0'; 
       Found <= '0'; 
       enables <= "00";
       init <= '0';
       data_enable <= '0';

       CASE y IS
          WHEN InitLow =>
            enables(0) <= '1';
            init <= '1';
          WHEN InitHigh =>
            enables(1) <= '1';
            init <= '1';
          WHEN MemoryRequest =>
          WHEN DataStore =>
             data_enable <= '1';
          WHEN DataInspect =>
             IF (data_reg < Data) THEN
               enables(0) <= '1'; -- change low to addr + 1
             ELSIF (data_reg > Data) THEN
               enables(1) <= '1'; -- change high to addr - 1
             END IF;
          WHEN Finish =>
            Done <= '1';
            IF (data_reg = Data) THEN
              Found <= '1';
            END IF;
       END CASE;
    END PROCESS;


    fsmflipflops: PROCESS(Clock, Resetn)
    BEGIN
      IF (Resetn = '0') THEN
        y <= InitLow;
      ELSIF (Clock'event AND Clock = '1') THEN
        y <= y_next;
      END IF;
    END PROCESS;


END Behavior ;

LIBRARY ieee ;
USE ieee.std_logic_1164.all ;

-- n-bit register with synchronous reset and enable
ENTITY regne IS
    GENERIC ( N : INTEGER := 5 ) ;
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
