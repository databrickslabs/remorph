-- see https://docs.snowflake.com/en/sql-reference/operators-logical

SELECT NOT FALSE OR TRUE, (NOT FALSE) OR TRUE, NOT (FALSE OR TRUE);