<!-- SPDX-License-Identifier: zlib-acknowledgement -->
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
