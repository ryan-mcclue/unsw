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
