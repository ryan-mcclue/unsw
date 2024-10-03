<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Sequential circuits (FSMs) have state (while combinational just input and output).
So, will involve flipflops.

TODO: glitching gives potential to save more time; 
however wanted clocked output for I/O

```
  -- determined 8bits for one-hot encoded state 
  -- at state table, see each next state bit and how it relates to next state to get logic expressions
  next_state(0) <= cur_state(0) and input
```

Moore machine input affects state transition, not output.
```
case state is
  when S0 =>
    if coin = '1' then
      next_state <= S1
    end if;
    output <= '0'
end case;
```
Mealy (just Moore with extras)
```
architecture mealy_fsm_arch of mealy_fsm is
  type state_type : S0, S1, S2, S3;
  signal state : state_type;
  constant HIHG : unsigned(3 downto 0) := "1001";
begin
process (clk, async_reset)
begin
  if reset = '1' then
    output <= "00";
  elsif rising_edge(clk) then
    case state is
      when S0 =>
        if coin = '1' then
          next_state <= S1
          output <= '1'
        else
          output <= '0'
        end if;
    end case;
  end if;
end process;
```
