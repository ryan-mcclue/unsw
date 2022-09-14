ENTITY func1 IS
  PORT (x1, x2, x3: IN BIT;
        f: OUT BIT);
END func1;

ARCHITECTURE logic_func OF func1 IS
BEGIN
  f <= (NOT x1 AND x2) OR
       (NOT x3 AND x1);
END logic_func;
