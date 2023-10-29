-- see https://docs.snowflake.com/en/sql-reference/functions/regr_valx

SELECT col_y, col_x, REGR_VALX(col_y, col_x), REGR_VALY(col_y, col_x)
    FROM xy;