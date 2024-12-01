-------------------------------------------------------------------------------
--
--  2024 COMP3222/9222 PRACTICE PRACTICAL EXAM
--
--  Please complete your name and zID to avoid misidentifying your work!
--
--  Student name:
--  Student zID:
--
-------------------------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.std_logic_unsigned.all;
USE work.definitions.all;

ENTITY hilo IS
    PORT( -------------------------------------------------------------------------------
          -- clk : IN std_logic;    -- COMMENT OUT when simulating and UNCOMMENT the following line
          btnC : IN std_logic;   -- COMMENT OUT for free-running clock and UNCOMMENT the previous line
          -------------------------------------------------------------------------------
          btnL, btnR : IN std_logic;                  -- load and reset inputs
          sw : IN std_logic_vector(9 DOWNTO 0);       -- num input
          seg : out STD_LOGIC_VECTOR (0 TO 6);        -- display segments
          an : out STD_LOGIC_VECTOR (3 DOWNTO 0));    -- display anodes (select bits)
END hilo;

ARCHITECTURE behavioural OF hilo IS
    COMPONENT debounce is    -- debounce code - instantiate when implementing on the board;
        PORT( clk : IN std_logic;    -- do not instantiate when simulating your FSM
              noisy_sig : IN std_logic;
              clean_sig : OUT std_logic);
    END COMPONENT;
    SIGNAL clk_divider : std_logic_vector(17 DOWNTO 0) := "000000000000000000";
    SIGNAL disp0, disp1, disp2, disp3 : std_logic_vector(0 TO 6);    -- four 7-seg display segments

    SIGNAL load, reset, resetn : std_logic;
    SIGNAL num: std_logic_vector(9 DOWNTO 0);

	SIGNAL dm : DISPLAY_MSG_TYPE;	-- type defined in package.vhd

	SIGNAL count: std_logic_vector(9 DOWNTO 0);	 -- guess number
	SIGNAL target: std_logic_vector(9 DOWNTO 0);  -- target value
	SIGNAL guess: std_logic_vector(9 DOWNTO 0);  -- guess value

-------------------------------------------------------------------------------
--  COMMENT OUT FOLLOWING LINE FOR FREE-RUNNING CLOCK; UNCOMMENT WHEN SIMULATING
    SIGNAL clk : std_logic;
-------------------------------------------------------------------------------

-- ADD YOUR SIGNAL DEFINITIONS BELOW


	

BEGIN

--  COMMENT OUT THE FOLLOWING 3 LINES for free-running clock; UNCOMMENT when simulating
    clk <= btnC;
    resetn <= NOT btnR;
    load <= btnL;

--  COMMENT OUT THE FOLLOWING 3 LINES WHEN SIMULATING; UNCOMMENT for free-running clock
--    rst: debounce PORT MAP( clk, btnR, reset);
--    resetn <= NOT reset;
--    ld: debounce PORT MAP( clk, btnL, load);

    num <= sw;
    
    -- DO NOT MODIFY THE FOLLOWING INSTANTIATED COMPONENT
    -- display message on 7-segment displays according to the display message type
    dc: display_controller PORT MAP ( 
        dm => dm,  -- display message type
        count => count,  -- guess number
        target => target,  -- target value
        guess => guess,  -- guess value
        disp0 => disp0,  -- 7-seg displays
        disp1 => disp1,
        disp2 => disp2,
        disp3 => disp3 );

    -- ADD YOUR CONTROL PATH DESCRIPTION AS NEEDED BELOW THIS LINE
    target_reg: regn GENERIC MAP (n => 8) PORT MAP (target_enable, '0', sw(9 DOWNTO 0), target);
    guess_reg: regn GENERIC MAP (n => 8) PORT MAP (target_enable, '0', sw(9 DOWNTO 0), target);
    guess_count_reg: regn GENERIC MAP (n => 8) PORT MAP (target_enable, '0', sw(9 DOWNTO 0), target);

    PROCESS (y, load)
    BEGIN
      CASE y IS 
        WHEN WaitForLoad =>
          IF (load = '1') THEN
            y_next <= Load;
          END IF;
        WHEN Load =>
          IF (load = '0') THEN
            y_next <= Try;
          END IF;
        WHEN Try =>
          IF (load = '1') THEN
            y_next <= LoadGuess;
          END IF;
        WHEN LoadGuess =>
          IF (load = '0') THEN
            y_next <= CompareGuess;
          END IF;
        WHEN CompareGuess =>
          IF (guess < target) THEN
            y_next <= Low;
          ELSE IF (guess > target) THEN
            y_next <= High; 
          END IF;
        WHEN Low =>
          y_next <= WaitForLoadGuess;
        WHEN OTHERS =>
      END CASE;
    END PROCESS;


    PROCESS (y)
    BEGIN
      target_enable <= '0';
      CASE y IS
        WHEN WaitForTargetLoad =>
         dm <= disp_load;
        WHEN TargetLoad =>
         dm <= disp_tv; 
         target_enable <= '1';
        WHEN WaitForGuessLoad =>
        WHEN GuessLoad =>
          guess_counter_enable <= '1';
          guess_enable <= '1';
        WHEN GuessCompare =>
        WHEN LowGuess =>
         dm <= disp_low;
        WHEN HighGuess =>
        WHEN Finished =>
          dm <= disp_fin;
      END CASE;
    END PROCESS;

    -- ADD YOUR DATAPATH DESCRIPTION AS NEEDED BELOW THIS LINE



	
-------------------------------------------------------------------------------
-- OUTPUT TO 7-SEGMENT DISPLAYS - DO NOT EDIT ARCHITECTURE BELOW THIS LINE
-------------------------------------------------------------------------------

    clk_div: PROCESS (clk) -- set up high frequency strobe signal to ensure flicker-free output
    BEGIN
        IF (clk'event AND clk = '1') THEN
            clk_divider <= clk_divider + 1;
        END IF;
    END PROCESS;
    
    WITH clk_divider(17 DOWNTO 16) SELECT -- determine which digit to display
        seg <= disp0 WHEN "00",
               disp1 WHEN "01",
               disp2 WHEN "10",
               disp3 WHEN OTHERS;

    an(0) <= clk_divider(17) OR clk_divider(16); -- determine when to display each digit
    an(1) <= clk_divider(17) OR NOT(clk_divider(16));
    an(2) <= NOT(clk_divider(17)) OR clk_divider(16);
    an(3) <= NOT(clk_divider(17)) OR NOT(clk_divider(16));

END behavioural;

LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.std_logic_unsigned.all;

ENTITY debounce IS
    PORT( clk : IN std_logic;
          noisy_sig : IN std_logic;
          clean_sig : OUT std_logic);
END debounce;

ARCHITECTURE behavioural OF debounce IS
    SIGNAL input_prev : std_logic;
    SIGNAL synch_count : std_logic_vector(20 DOWNTO 0);
BEGIN
    synchronize: PROCESS
    BEGIN
        WAIT UNTIL clk'event AND clk = '1';
        input_prev <= noisy_sig;
        IF noisy_sig /= input_prev THEN
            synch_count <= (others => '0');
        ELSIF synch_count /= x"100000" THEN
            synch_count <= synch_count + 1;
        END IF;
        IF synch_count = x"100000" THEN
            clean_sig <= noisy_sig;
        END IF;
    END PROCESS;
END behavioural;
