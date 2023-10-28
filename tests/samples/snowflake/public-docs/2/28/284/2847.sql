CREATE PROCEDURE case_demo_01(v VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
  BEGIN
    CASE (v)
      WHEN 'first choice' THEN
        RETURN 'one';
      WHEN 'second choice' THEN
        RETURN 'two';
      ELSE
        RETURN 'unexpected choice';
    END;
  END;