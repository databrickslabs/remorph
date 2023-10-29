-- see https://docs.snowflake.com/en/sql-reference/functions/regr_valx

SELECT REGR_VALX(NULL, 10), REGR_VALX(1, NULL), REGR_VALX(1, 10);