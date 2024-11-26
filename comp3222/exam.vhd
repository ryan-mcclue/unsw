-- TIMER
ENTITY half_sec_timer IS
    PORT( Clk, Start : IN std_logic;
          Done : OUT std_logic);
END half_sec_timer;

ARCHITECTURE Behavior OF half_sec_timer IS
    SIGNAL Q : INTEGER RANGE 0 TO 50000000;
BEGIN
    PROCESS (Clk)
    BEGIN
        IF (Clk'event AND Clk = '1') THEN
            IF (Start = '1') THEN    -- initialize timer when Start asserted
                Done <= '0';
                Q <= 0;
            ELSIF (Q = 50000000) THEN    -- assert Done when 0.5 seconds elapsed
                Done <= '1';
                Q <= 0;
            ELSE    -- increment timer each cycle
                Done <= '0';
                Q <= Q + 1;
            END IF;
        END IF;
    END PROCESS;
END Behavior;


-- COUNTER
ENTITY counter IS
  PORT (enable, reset, clk: IN STD_LOGIC;
        q: BUFFER STD_LOGIC_VECTOR(3 DOWNTO 0));
END counter;

ARCHITECTURE behav OF counter IS
BEGIN
   PROCESS (clk) BEGIN
     IF (clk'event = '1' and clk = '1') THEN
       q <= q + 1;   
     END IF;
   END PROCESS;
END behav;

-- REGISTER
COMPONENT regn IS
GENERIC( n : INTEGER := 9);
PORT( R : IN std_logic_vector(n-1 DOWNTO 0);
      Rin, Clock : IN std_logic;
      Q : BUFFER std_logic_vector(n-1 DOWNTO 0));
END COMPONENT;

LIBRARY ieee;
USE ieee.std_logic_1164.all;

ENTITY regn IS
    GENERIC( n : INTEGER := 9);
    PORT( R : IN std_logic_vector(n-1 DOWNTO 0);
          Rin, Clock : IN std_logic;
          Q : BUFFER std_logic_vector(n-1 DOWNTO 0));
END regn;

ARCHITECTURE Behavior OF regn IS
BEGIN
    PROCESS( Clock)
    BEGIN
        IF (Clock'event AND Clock = '1') THEN
            IF (Rin = '1') THEN
                Q <= R;
            END IF;
        END IF;
    END PROCESS;
END Behavior;

-- SHIFT
address <= "0" & address_shift(5 DOWNTO 1);

ENTITY shiftrne IS
    GENERIC( N : INTEGER:=4);
    PORT( R : IN std_logic_vector(N-1 DOWNTO 0);
          L, E, w : IN std_logic;
          Clock : IN std_logic;
          Q : BUFFER std_logic_vector(N-1 DOWNTO 0));
END shiftrne ;

ARCHITECTURE Behavior OF shiftrne IS
BEGIN
    PROCESS
    BEGIN
        WAIT UNTIL (Clock'EVENT AND Clock = '1');
        IF (E = '1') THEN    -- only shift or load when enabled
            IF (L = '1') THEN    -- depending upon the load signal
                Q <= R;     -- either load a new word in parallel
            ELSE    -- or
                Genbits: FOR i IN 0 TO N-2 LOOP    -- shift the word to the right
                    Q(i) <= Q(i+1);
                END LOOP;
                Q(N-1) <= w;
            END IF;
        END IF;
    END PROCESS;
END Behavior;



-- MUX
WITH s SELECT
  f <= w0 WHEN "00",
       w1 WHEN "01",
       w2 WHEN "10",
       w3 WHEN OTHERS;

-- DECODER
COMPONENT dec3to8 IS
PORT( W : IN std_logic_vector(2 DOWNTO 0);
      En : IN std_logic;
      Y : OUT std_logic_vector(0 TO 7));
END COMPONENT;

ARCHITECTURE Behavior OF dec3to8 IS
BEGIN
    PROCESS( W, En)
    BEGIN
        IF (En = '1') THEN
            CASE W IS
                WHEN "000" =>  Y <= "10000000";
                WHEN "001" =>  Y <= "01000000";
                WHEN "010" =>  Y <= "00100000";
                WHEN "011" =>  Y <= "00010000";
                WHEN "100" =>  Y <= "00001000";
                WHEN "101" =>  Y <= "00000100";
                WHEN "110" =>  Y <= "00000010";
                WHEN "111" =>  Y <= "00000001";
                WHEN OTHERS => Y <= "00000000";
            END CASE;
        ELSE
            Y <= "00000000";
        END IF;
    END PROCESS;
END Behavior;

-- OVERFLOW
Sum <= ('0' & X) + (‘0’ & Y) + Cin ;
Overflow <= Sum(16) XOR X(15) XOR Y(15) XOR Sum(15);

-- CASCADE
G1: FOR i IN 0 TO 3 GENERATE
  muxes: mux2to1 PORT MAP (sw(4*i to i), m(0));
  G2: IF i=2 GENERATE
    muxother: mux3to1 PORT MAP (sw(4*i to i), m(0));
  END GENERATE;
END GENERATE;

-- STATE
TYPE State IS (InitLow, InitHigh, MemoryRequest, DataStore, DataInspect, Finish);
SIGNAL y, y_next: State;

CONSTANT SUB: STD_LOGIC_VECTOR := "011";

statetable: PROCESS(y, s)
BEGIN
    CASE y IS
        WHEN InitLow =>
            y_next <= InitHigh;
        WHEN InitHigh =>
            IF (s = '1') THEN
                y_next <= MemoryRequest; 
            END IF; 
        WHEN OTHERS =>
    END CASE;
END PROCESS;

controlsignals: PROCESS(y)
BEGIN
   Done <= '0'; Found <= '0'; enables <= "00";
   CASE y IS
      WHEN InitLow =>
        enables(0) <= '1';
        init <= '1';
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

addresscalc: PROCESS(low_reg, high_reg, address_shift)
BEGIN
  address_shift <= (high_reg + low_reg);
  address <= "0" & address_shift(5 DOWNTO 1);
END PROCESS;


