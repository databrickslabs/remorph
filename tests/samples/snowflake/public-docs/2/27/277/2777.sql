CREATE PROCEDURE null_as_statement()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
    SELECT 1 / 0;
    RETURN 'If you see this, the exception was not thrown/caught properly.';
EXCEPTION
    WHEN OTHER THEN
        NULL;
END;
$$
;