<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Sequential circuits (FSMs) have state (while combinational just input and output).
So, will involve flipflops.

Moore machine input affects state transition, not output:
IMPORTANT: moore most common as synchronous circuit
```
case state is
  when S0 =>
    if coin = '1' then
      next_state <= S1
    end if;
    output <= '0'
end case;
```
Mealy:
```
case state is
  when S0 =>
    if coin = '1' then
      next_state <= S1
      output <= '1'
    else
      output <= '0'
    end if;
end case;
```
