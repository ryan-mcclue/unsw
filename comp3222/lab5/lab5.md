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
