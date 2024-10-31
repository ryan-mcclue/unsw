<!-- SPDX-License-Identifier: zlib-acknowledgement -->
IMPORTANT: all 'inputs' must appear in senstitivity list

Digital systems have datapath (adders, muxes, registers, decoders etc.) 
which feed into controller (FSM) that feeds back into datapath.
(these datapath elements are often components like shiftleft, mux, downcnt etc.)

This is encoded in an algorithmic state machine (ASM).
Has state box, decision box, conditional output box



Register Q outputs share bus through 3-state buffer.
So, controller asserts the control signal on buffer for output register.
and enable signal for input register.

IR: xxx (op) xxx (r0) xxx (r1)

to determine reg number, pass bit pattern to 3-8decoder

TODO: how to wait for Din input after decoding mvi?


0. load IR
run signal = 1
done signal (finished)
'IRin <= 1'
1. mov r0, r1:
'muxReg1Select/reg1Out' <= 1; 'reg0Enable/reg0In' <= 1; 
2. mov r0, #d (multiple cycles to first decode D and then load immediate)
'muxDSelect', 'reg0Enable'
3. add r0, r1
muxReg0Select, regAEnable (accumulator)
muxReg1Select, regGEnable (ALU result), addSignal
muxGSelect, reg0Enable

```
state, nextState

PROCESS (Clk, nReset)
BEGIN
    IF (nReset = '0') THEN
        TStep_Q <= T0;
    ELSIF (Clk'event AND Clk = '1') THEN
        TStep_Q <= TStep_D;
    END IF;
END PROCESS;


BusWires: BUFFER 	STD_LOGIC_VECTOR(8 DOWNTO 0));
SIGNAL RegisterIns STD_LOGIC_VECTOR(8 DOWNTO 0));
SIGNAL RegisterOuts STD_LOGIC_VECTOR(8 DOWNTO 0));
SIGNAL R0, R2, ... R7, IR, GR, AR: STD_LOGIC_VECTOR(8 DOWNTO 0));

reg0: regn GENERIC MAP ( n => 9 )
			PORT MAP (BusWires, RegisterIns(0), Clock, r0);
ir: (Din, IRin, Clock, IR)

alu: alu PORT MAP (AddSub, AR, BusWires, GR); 

-- add GOut and Dout to RegOut
-- mux (bus definition)
PROCESS (RegOut, Din, R0, ..., R7, GR)
BEGIN
  IF (RegOut(REG_0) = '1') THEN
    BusWires <= R0;
  ELSIF ...
  ELSE
    BusWires <= Din;
  END IF;
END PROCESS;

```


include transitions, outputs and datapath activities.
```
S0: waiting for instruction
S1: Load rx from data
```






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
    SIGNAL R0, R1, R2, R3, R4, R5, R6, R7, IR, GR, AR: STD_LOGIC_VECTOR(8 DOWNTO 0);
    
    SIGNAL GeneralPurposeIns: STD_LOGIC_VECTOR(0 TO 7);
    SIGNAL IRin: STD_LOGIC;
    
    -- Controlled with FSM, only R0-R7, G, signaz
    
    SIGNAL GeneralPurposeOuts: STD_LOGIC_VECTOR(0 TO 7);
    SIGNAL DinOut, GOut, AOut: STD_LOGIC;
    
    CONSTANT MV: STD_LOGIC_VECTOR := "000";
    CONSTANT MVI: STD_LOGIC_VECTOR := "001";
    CONSTANT ADD: STD_LOGIC_VECTOR := "010";
    CONSTANT SUB: STD_LOGIC_VECTOR := "100";
    
    -- Instruction opcode
    SIGNAL I: STD_LOGIC_VECTOR(2 DOWNTO 0);
    
    -- Register operands
    SIGNAL Xreg, Yreg: STD_LOGIC_VECTOR(0 TO 7);
    
BEGIN
    Hi <= '1';
    I <= IR(8 DOWNTO 6);
    decX: dec3to8 PORT MAP( IR(5 DOWNTO 3), Hi, Xreg);
    decY: dec3to8 PORT MAP( IR(2 DOWNTO 0), Hi, Yreg);

    statetable: PROCESS( Tstep_Q, Run, I)
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

    controlsignals: PROCESS( Tstep_Q, I, Xreg, Yreg)
    BEGIN
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
                   WHEN SUB =>
                     
                   WHEN ADD => 
                   
                   WHEN OTHERS =>
                END CASE;
            WHEN T2 =>
               CASE I IS
                  WHEN ADD =>
                    -- as only 1 step, define here
                     Done <= '1';
                   WHEN OTHERS =>
                END CASE;
            
             -- define signals in time step T2
            WHEN T3 => -- define signals in time step T3
        END CASE;
    END PROCESS;

    fsmflipflops: PROCESS( Clock, Resetn)
    BEGIN
      IF (Resetn = '0') THEN
        TStep_Q <= T0;
      ELSIF (Clock'event AND Clock = '1') THEN
        TStep_Q <= TStep_D;
      END IF;
    END PROCESS;
	
    -- instantiate registers and the adder/subtracter unit
    reg_0: regn PORT MAP( BusWires, GeneralPurposeIns(0), Clock, R0);
    -- generate general purpose
    reg_A: regn PORT MAP( BusWires, ARIn, Clock, AR);
    reg_IR: regn PORT MAP( BusWires, IRIn, Clock, IR);
    
    alu: WITH AddSub SELECT
         Sum <= A + BusWires WHEN '0',
         A - BusWires WHEN OTHERS ;
    reg_G: regn PORT MAP( BusWires, GRIn, Clock, GR);

    -- define the bus
    
    -- TODO: look at lecture slides for code!!
    muxes: WITH GeneralPurposeOuts & GROut & DROut
    BusWires <= R0 WHEN "1000000000",
                R1 WHEN "100",
                R1 WHEN "010",
                R3 WHEN OTHERS ;
    
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

