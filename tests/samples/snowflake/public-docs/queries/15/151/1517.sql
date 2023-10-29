-- see https://docs.snowflake.com/en/sql-reference/operators-logical

SELECT TRUE OR TRUE AND FALSE, TRUE OR (TRUE AND FALSE), (TRUE OR TRUE) AND FALSE;