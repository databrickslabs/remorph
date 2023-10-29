-- see https://docs.snowflake.com/en/sql-reference/functions/regr_valy

SELECT REGR_VALY(NULL, 10), REGR_VALY(1, NULL), REGR_VALY(1, 10);