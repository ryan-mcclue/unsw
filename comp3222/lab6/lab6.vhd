-------------------------------------------------------------------------------
--
--  Describes processor from l6p1 for simulation
--
-------------------------------------------------------------------------------

LIBRARY ieee; 
USE ieee.std_logic_1164.all;
USE ieee.std_logic_signed.all;

ENTITY l6p1sim IS
    PORT( DIN : IN std_logic_vector(8 DOWNTO 0);
          Resetn, Clock, Run : IN std_logic;
          Done : BUFFER std_logic;
          BusWires : BUFFER std_logic_vector(8 DOWNTO 0));
END l6p1sim;

ARCHITECTURE Mixed OF l6p1sim IS
-- declare components
    COMPONENT dec3to8 IS
    PORT( W : IN std_logic_vector(2 DOWNTO 0);
          En : IN std_logic;
          Y : OUT std_logic_vector(0 TO 7));
    END COMPONENT;
    COMPONENT regn IS
    GENERIC( n : INTEGER := 9);
    PORT( R : IN std_logic_vector(n-1 DOWNTO 0);
          Rin, Clock : IN std_logic;
          Q : BUFFER std_logic_vector(n-1 DOWNTO 0));
    END COMPONENT;

-- declare signals
    TYPE State_type IS (T0, T1, T2, T3);
    SIGNAL Tstep_Q, Tstep_D: State_type;
    
    SIGNAL Hi: STD_LOGIC;
    SIGNAL R0, R1, R2, R3, R4, R5, R6, R7, IR, GR, AR, DIN: STD_LOGIC_VECTOR(8 DOWNTO 0);
    
    SIGNAL GeneralPurposeIns: STD_LOGIC_VECTOR(0 TO 7);
    SIGNAL IRin, ARin, GRin: STD_LOGIC;

    SIGNAL GeneralPurposeOuts: STD_LOGIC_VECTOR(0 TO 7);
    SIGNAL DINOut, GROut: STD_LOGIC;

    SIGNAL Sel: STD_LOGIC_VECTOR(0 TO 9);
    
    -- Define instructions
    CONSTANT MV: STD_LOGIC_VECTOR := "000";
    CONSTANT MVI: STD_LOGIC_VECTOR := "001";
    CONSTANT ADD: STD_LOGIC_VECTOR := "010";
    CONSTANT SUB: STD_LOGIC_VECTOR := "011";
    
    -- Instruction opcode
    SIGNAL I: STD_LOGIC_VECTOR(2 DOWNTO 0);
    
    -- Register operands
    SIGNAL Xreg, Yreg: STD_LOGIC_VECTOR(0 TO 7);

    -- Adder control signal
    SIGNAL AddSub: STD_LOGIC;
    SIGNAL Sum: STD_LOGIC_VECTOR(8 DOWNTO 0);
    
BEGIN
    Hi <= '1';
    I <= IR(8 DOWNTO 6);
    decX: dec3to8 PORT MAP(IR(5 DOWNTO 3), Hi, Xreg);
    decY: dec3to8 PORT MAP(IR(2 DOWNTO 0), Hi, Yreg);

    statetable: PROCESS(Tstep_Q, Run, I)
    BEGIN
        CASE Tstep_Q IS
            WHEN T0 => -- data is loaded into IR in this time step
                IF (Run = '0') THEN
                    Tstep_D <= T0;
                ELSE 
                    Tstep_D <= T1;
                END IF; 
            WHEN T1 =>
              IF (I = MVI OR I = MV) THEN
                  Tstep_D <= T0;
              ELSE 
                  Tstep_D <= T2;
              END IF; 
            WHEN T2 =>
              Tstep_D <= T3;
            WHEN T3 =>
              Tstep_D <= T0;
        END CASE;
    END PROCESS;

    controlsignals: PROCESS(Tstep_Q, I, Xreg, Yreg)
    BEGIN
       -- Clear all outputs
       Done <= '0'; 
       GeneralPurposeIns <= (OTHERS => '0'); 
       IRin <= '0'; ARIn <= '0'; GRIn <= '0';
       GeneralPurposeOuts <= (OTHERS => '0'); 
       DINOut <= '0'; GROut <= '0';
       AddSub <= '0'; 

        -- specify initial values
        CASE Tstep_Q IS
            WHEN T0 => -- store DIN in IR as long as Tstep_Q = 0
                IRin <= '1';
            WHEN T1 => -- define signals in time step T1
                CASE I IS
                   WHEN MV =>
                     GeneralPurposeOuts <= Yreg;
                     GeneralPurposeIns <= Xreg;
                     -- as only 1 step, define here
                     Done <= '1';
                   WHEN MVI =>
                     DinOut <= '1'; -- Din should be in at this point
                     GeneralPurposeIns <= Xreg;
                     Done <= '1';
                   WHEN ADD => 
                     GeneralPurposeOuts <= Xreg;
                     Ain <= '1';
                   WHEN SUB =>
                     GeneralPurposeOuts <= Xreg;
                     Ain <= '1';
                   WHEN OTHERS =>
                END CASE;
            WHEN T2 =>
               CASE I IS
                  WHEN ADD =>
                     GeneralPurposeOuts <= Yreg; 
                     Gin <= '1'; 
                  WHEN SUB =>
                     GeneralPurposeOuts <= Yreg; 
                     Gin <= '1'; 
                     AddSub <= '1';
                  WHEN OTHERS =>
                END CASE;
            WHEN T3 => 
              CASE I IS
                  WHEN ADD =>
                     Gout <= '1'; 
                     GeneralPurposeIns <= Xreg; 
                     Done <= '1';
                  WHEN SUB =>
                     Gout <= '1'; 
                     GeneralPurposeIns <= Xreg; 
                     Done <= '1';
                  WHEN OTHERS =>
              END CASE;
        END CASE;
    END PROCESS;

    fsmflipflops: PROCESS(Clock, Resetn)
    BEGIN
      IF (Resetn = '0') THEN
        Tstep_Q <= T0;
      ELSIF (Clock'event AND Clock = '1') THEN
        Tstep_Q <= Tstep_D;
      END IF;
    END PROCESS;
	
    -- instantiate registers and the adder/subtracter unit
    reg_0: regn PORT MAP (BusWires, GeneralPurposeIns(0), Clock, R0);
    reg_1: regn PORT MAP (BusWires, GeneralPurposeIns(1), Clock, R1);
    reg_2: regn PORT MAP (BusWires, GeneralPurposeIns(2), Clock, R2);
    reg_3: regn PORT MAP (BusWires, GeneralPurposeIns(3), Clock, R3);
    reg_4: regn PORT MAP (BusWires, GeneralPurposeIns(4), Clock, R4);
    reg_5: regn PORT MAP (BusWires, GeneralPurposeIns(5), Clock, R5);
    reg_6: regn PORT MAP (BusWires, GeneralPurposeIns(6), Clock, R6);
    reg_7: regn PORT MAP (BusWires, GeneralPurposeIns(7), Clock, R7);
    reg_IR: regn PORT MAP (DIN, IRIn, Clock, IR);
    reg_A: regn PORT MAP (BusWires, ARIn, Clock, AR);
    reg_G: regn PORT MAP (BusWires, GRIn, Clock, GR);
    
    alu: WITH AddSub SELECT
         Sum <= AR + BusWires WHEN '0',
                AR - BusWires WHEN OTHERS;
    reg_G: regn PORT MAP (Sum, GRIn, Clock, GR);

    -- define the bus
    Sel <= GeneralPurposeOuts & GROut & DROut;
    muxes: WITH Sel SELECT
        BusWires <= R0 WHEN "1000000000",
                    R1 WHEN "0100000000",
                    R2 WHEN "0010000000",
                    R3 WHEN "0001000000",
                    R4 WHEN "0000100000",
                    R5 WHEN "0000010000",
                    R6 WHEN "0000001000",
                    R7 WHEN "0000000100",
                    GR WHEN "0000000010",
                    DIN WHEN OTHERS;
    
END PROCESS;

END Mixed;

LIBRARY ieee;
USE ieee.std_logic_1164.all;

ENTITY dec3to8 IS
    PORT( W : IN std_logic_vector(2 DOWNTO 0);
          En : IN std_logic;
          Y : OUT std_logic_vector(0 TO 7));
END dec3to8;

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

