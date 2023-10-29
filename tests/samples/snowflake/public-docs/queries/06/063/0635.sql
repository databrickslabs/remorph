-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/begin

EXECUTE IMMEDIATE $$
BEGIN
    BEGIN TRANSACTION;
    TRUNCATE TABLE child;
    TRUNCATE TABLE parent;
    COMMIT;
    RETURN '';
END;
$$
;