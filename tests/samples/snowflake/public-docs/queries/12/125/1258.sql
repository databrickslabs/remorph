-- see https://docs.snowflake.com/en/sql-reference/operators-logical

SELECT NOT FALSE AND FALSE, (NOT FALSE) AND FALSE, NOT (FALSE AND FALSE);