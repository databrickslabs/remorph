-- see https://docs.snowflake.com/en/sql-reference/identifier-literal

CREATE FUNCTION speed_of_light() 
RETURNS INTEGER
AS
    $$
    299792458
    $$;