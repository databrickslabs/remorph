-- see https://docs.snowflake.com/en/sql-reference/session-variables

SET (VAR1, VAR2, VAR3)=(10, 20, 30);
SET (VAR1, VAR2, VAR3)=(SELECT 10, 20, 30);