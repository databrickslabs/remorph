DECLARE
  counter1 NUMBER(8, 0);
  counter2 NUMBER(8, 0);
BEGIN
  counter1 := 0;
  counter2 := 0;
  WHILE (counter1 < 3) DO
    counter1 := counter1 + 1;
    CONTINUE;
    counter2 := counter2 + 1;
  END WHILE;
  RETURN counter2;
END;