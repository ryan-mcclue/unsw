-- TODO: why this one only 'y', i.e no y_Q and y_D?
-- TODO: are condition boxes for external operations, like load or increment?

-------------------------------------------------------------------------------
--
-- implement the 'popcount' function using the ASM depicted in Lab 7 Fig 1
--
-------------------------------------------------------------------------------
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;
USE ieee.std_logic_unsigned.all ;

ENTITY l7p1 IS
    PORT( Clock, Resetn	: IN STD_LOGIC ;
          s	: IN STD_LOGIC ;
          Data : IN STD_LOGIC_VECTOR(7 DOWNTO 0) ;
          B : BUFFER STD_LOGIC_VECTOR(3 DOWNTO 0) ;
          Done : OUT STD_LOGIC ) ;
END l7p1;

ARCHITECTURE Behavior OF l7p1 IS
    COMPONENT shiftrne IS -- left-to-right shift register with load and enable
        GENERIC ( N : INTEGER := 4 ) ;
        PORT( Data : IN STD_LOGIC_VECTOR(N-1 DOWNTO 0);
              Load, Enable, ShiftIn, Clock : IN	STD_LOGIC ;
              Q : BUFFER STD_LOGIC_VECTOR(N-1 DOWNTO 0) ) ;
    END COMPONENT ;
    TYPE State_type IS ( S1, S2, S3 ) ;
    SIGNAL y : State_type ;
    SIGNAL LA: STD_LOGIC;
    SIGNAL A : STD_LOGIC_VECTOR(7 DOWNTO 0) ;
    SIGNAL z, EA, LB, EB, low : STD_LOGIC ;
BEGIN
    FSM_transitions: PROCESS ( Resetn, Clock )
    BEGIN
        IF Resetn = '0' THEN
            y <= S1 ;
        ELSIF (Clock'EVENT AND Clock = '1') THEN
            CASE y IS
                WHEN S1 =>
                    IF s = '0' THEN 
                        y <= S1 ; 
                    ELSE 
                        y <= S2 ; 
                    END IF ;
                WHEN S2 =>
                    IF z = '0' THEN 
                        y <= S2 ; 
                    ELSE 
                        y <= S3 ; 
                    END IF ;
                WHEN S3 =>
                    IF s = '1' THEN 
                        y <= S3 ; 
                    ELSE 
                        y <= S1 ; 
                    END IF ;
            END CASE ;
        END IF ;
    END PROCESS ;

    FSM_outputs: PROCESS ( y, A(0) )
    BEGIN
        EA <= '0' ; LB <= '0' ; EB <= '0' ; Done <= '0' ; LA <= '0';
        -- LA <= '0';
        CASE y IS
            WHEN S1 =>
                LB <= '1';
                IF (s = '0') THEN
                    LA <= '1';
                END IF;
            WHEN S2 =>
                EA <= '1' ;
                IF A(0) = '1' THEN 
                    EB <= '1' ; 
                END IF ;
            WHEN S3 =>
                Done <= '1' ;
        END CASE ;
    END PROCESS ;

    -- The datapath circuit is described below
    upcount: PROCESS ( Resetn, Clock )
    BEGIN
        IF Resetn = '0' THEN
            B <= "0000" ;
        ELSIF (Clock'EVENT AND Clock = '1') THEN
            IF LB = '1' THEN
                B <= "0000" ;
            ELSIF EB = '1' THEN 
                B <= B + '1' ;
            END IF ;
        END IF;
    END PROCESS;

    low <= '0' ;
    ShiftA: shiftrne GENERIC MAP ( N => 8 )
        PORT MAP ( Data, LA, EA, low, Clock, A ) ;
    z <= '1' WHEN A = "00000000" ELSE '0' ;			

END Behavior ;

LIBRARY ieee ;
USE ieee.std_logic_1164.all ;

ENTITY shiftrne IS -- left-to-right shift register with load & enable
    GENERIC ( N : INTEGER := 4 ) ;
    PORT( Data : IN STD_LOGIC_VECTOR(N-1 DOWNTO 0);
          Load, Enable, ShiftIn, Clock : IN	STD_LOGIC ;
          Q : BUFFER STD_LOGIC_VECTOR(N-1 DOWNTO 0) ) ;
END shiftrne ;

ARCHITECTURE Behavior OF shiftrne IS	
BEGIN
    PROCESS ( Clock )
    BEGIN
        IF Clock'EVENT AND Clock = '1' THEN
            IF Load = '1' THEN
                Q <= Data;
            ELSIF Enable = '1' THEN
                Genbits: FOR i IN N-2 DOWNTO 0 LOOP
                    Q(i) <= Q(i+1) ;
                END LOOP ;
                Q(N-1) <= ShiftIn ;
            END IF;
        END IF ;
    END PROCESS ;
END Behavior ;
