CREATE PROCEDURE case_demo_2(v VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
  BEGIN
    CASE
      WHEN v = 'first choice' THEN
        RETURN 'one';
      WHEN v = 'second choice' THEN
        RETURN 'two';
      ELSE
        RETURN 'unexpected choice';
    END;
  END;