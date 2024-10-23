<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1.
| state | next_state (w=0 \| w=1) | output |
|-------|-------------------------|--------|
| A     | B \| F                  | 0      |
| B     | C \| F                  | 0      |
| C     | D \| F                  | 0      |
| D     | E \| F                  | 0      |
| E     | E \| F                  | 1      |
| F     | B \| G                  | 0      |
| G     | B \| H                  | 0      |
| H     | B \| I                  | 0      |
| I     | B \| I                  | 1      |

TODO: Try to express in words what made you think the logic expression is what you claim it to be!

CONSTANT STATE_A : INTEGER := 0;
CONSTANT STATE_B : INTEGER := 1;
CONSTANT STATE_C : INTEGER := 2;
CONSTANT STATE_D : INTEGER := 3;
CONSTANT STATE_E : INTEGER := 4;
CONSTANT STATE_F : INTEGER := 5;
CONSTANT STATE_G : INTEGER := 6;
CONSTANT STATE_H : INTEGER := 7;
CONSTANT STATE_I : INTEGER := 8;

D(STATE_B) <= (Q(STATE_A) AND NOT w) OR (Q(STATE_F) AND NOT w) OR (Q(STATE_G) AND NOT w) OR (Q(STATE_H) AND NOT w) OR (Q(STATE_I) AND NOT w);
D(STATE_C) <= (Q(STATE_B) AND NOT w); 
D(STATE_D) <= (Q(STATE_C) AND NOT w); 
D(STATE_E) <= (Q(STATE_D) AND NOT w) OR (Q(STATE_E) AND NOT w);
D(STATE_F) <= (Q(STATE_A) AND w) OR (Q(STATE_B) AND w) OR (Q(STATE_C) AND w) OR (Q(STATE_D) AND w) OR (Q(STATE_E) AND w);
D(STATE_G) <= (Q(STATE_F) AND w);
D(STATE_H) <= (Q(STATE_G) AND w);
D(STATE_I) <= (Q(STATE_H) AND w) OR (Q(STATE_I) AND w);

z <= Q(STATE_E) OR Q(STATE_I); 

## ORIGINAL
PROCESS (Clock)
BEGIN
  IF Clock'event AND Clock = '1' THEN
      IF nReset = '0' THEN
  	  Q(0) <= '1';
      ELSE
  	  Q(0) <= '0';
      END IF;
  END IF;
END PROCESS;
	
2.
Compiler automatically determines number of flip-flops and encoding for FSM.
i.e. will infer FSM usage and encode state type enum most appropriately.
e.g. for < 32 states, uses one-hot 
Others include sequential, gray encoding etc. (look at synthesis report)


PROCESS (y_Q, w)
BEGIN
  CASE y_Q IS
    WHEN A =>
      IF w = '0' THEN
        y_D <= B;
      ELSE
        y_D <= F;
      END IF;
    WHEN B =>
      IF w = '0' THEN
        y_D <= C;
      ELSE
        y_D <= F;
      END IF;
    WHEN C =>
      IF w = '0' THEN
        y_D <= D;
      ELSE
        y_D <= F;
      END IF;
    WHEN D =>
      IF w = '0' THEN
        y_D <= E;
      ELSE
        y_D <= F;
      END IF;
    WHEN E =>
      IF w = '0' THEN
        y_D <= E;
      ELSE
        y_D <= F;
      END IF;
    WHEN F =>
      IF w = '0' THEN
        y_D <= B;
      ELSE
        y_D <= G;
      END IF;
    WHEN G =>
      IF w = '0' THEN
        y_D <= B;
      ELSE
        y_D <= H;
      END IF;
    WHEN H =>
      IF w = '0' THEN
        y_D <= B;
      ELSE
        y_D <= I;
      END IF;
    WHEN I =>
      IF w = '0' THEN
        y_D <= B;
      ELSE
        y_D <= I;
      END IF;
  END CASE;
END PROCESS;

PROCESS (Clock)
BEGIN
  IF (Clock'EVENT AND Clock = '1') THEN
    IF (nReset = '0') THEN
      y_Q <= A;
    ELSE
      y_Q <= y_D;
    END IF;
  END IF;
END PROCESS;

z <= '1' WHEN (y_Q = E) OR (y_Q = I) ELSE '0';

## Before
INFO: [Synth 8-802] inferred FSM for state register 'y_Q_reg' in module 'l5p2'
---------------------------------------------------------------------------------------------------
                   State |                     New Encoding |                Previous Encoding 
---------------------------------------------------------------------------------------------------
                       a |                        000000001 |                             0000
                       f |                        000000010 |                             0101
                       g |                        000000100 |                             0110
                       h |                        000001000 |                             0111
                       i |                        000010000 |                             1000
                       b |                        000100000 |                             0001
                       c |                        001000000 |                             0010
                       d |                        010000000 |                             0011
                       e |                        100000000 |                             0100
---------------------------------------------------------------------------------------------------
INFO: [Synth 8-3354] encoded FSM with state register 'y_Q_reg' using encoding 'one-hot' in module 'l5p2'


## After
INFO: [Synth 8-802] inferred FSM for state register 'y_Q_reg' in module 'l5p2'
---------------------------------------------------------------------------------------------------
                   State |                     New Encoding |                Previous Encoding 
---------------------------------------------------------------------------------------------------
                       a |                             1111 |                             1111
                       f |                             1010 |                             1010
                       g |                             1001 |                             1001
                       h |                             1000 |                             1000
                       i |                             0111 |                             0111
                       b |                             1110 |                             1110
                       c |                             1101 |                             1101
                       d |                             1100 |                             1100
                       e |                             1011 |                             1011
---------------------------------------------------------------------------------------------------
INFO: [Synth 8-3354] encoded FSM with state register 'y_Q_reg' using encoding 'User encoding' in module 'l5p2'

Original design used 9 bits with one-hot encoding to represent state variable.
From A to I, encoding shifted 'hot' bit left, e.g. 0, 1, 2, 4, 8 etc. 

Modified design used 4bits to represent state variable. 
From A to I, encoding was 4bit twos-complement, e.g -1, -2, -3, -4, etc.
Accordingly, only bottom 4 leds used to output state.

4.
IMPORTANT: cannot have transition and output both have cases affecting same variable (so add new state)

   FSM_transitions: 
    PROCESS (y_Q, w, TDone)
    BEGIN
      CASE y_Q IS
        WHEN Init =>
          IF (w = '1') THEN
            y_D <= ReadLen;
          END IF;
        WHEN ReadLen =>
          IF (QL(0) = '1') THEN
            TStart <= '1';
            y_D <= CharacterPauseTimer;
          ELSE
            y_D <= Init;
          END IF;
        WHEN CharacterPauseTimer =>
          IF (TDone = '1') THEN
            y_D <= ReadCode;
          END IF;
        WHEN ReadCode =>
          TStart <= '1';
          IF (QC(0) = '1') THEN
            y_D <= Stage1OutputTimer;
          ELSE
            y_D <= Stage0OutputTimer;
          END IF;
        WHEN Stage1OutputTimer =>
          IF (TDone = '1') THEN
            TStart <= '1';
            y_D <= Stage0OutputTimer;
          END IF;
        WHEN Stage0OutputTimer =>
          IF (TDone = '1') THEN
            y_D <= Shift;
          END IF;
        WHEN Shift =>
          y_D <= ReadLen;
      END CASE;
    END PROCESS;


		
    FSM_state: 
    PROCESS (Clk, nReset)
    BEGIN
        IF (nReset = '0') THEN
            y_Q <= Init;
        ELSIF (Clk'event AND Clk = '1') THEN
            y_Q <= Y_D;
        END IF;
    END PROCESS;

-- complete the FSM outputs below
			
    FSM_outputs:
    PROCESS (y_Q)
    BEGIN
      SEnable <= '0'; TStart <= '0'; z <= '0';
      CASE y_Q IS
        WHEN Init =>
          SEnable <= '1';
        WHEN Shift =>
          SEnable <= '1';
        WHEN Stage1OutputTimer =>
          z <= '1';
        WHEN Stage0OutputTimer =>
          z <= '1';
        WHEN OTHERS =>
      END CASE;
    END PROCESS;
