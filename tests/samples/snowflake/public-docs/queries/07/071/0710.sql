-- see https://docs.snowflake.com/en/sql-reference/functions/nth_value

SELECT
        partition_col, order_col, i,
        FIRST_VALUE(i)  OVER (PARTITION BY partition_col ORDER BY order_col
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS FIRST_VAL,
        NTH_VALUE(i, 2) OVER (PARTITION BY partition_col ORDER BY order_col
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS NTH_VAL,
        LAST_VALUE(i)   OVER (PARTITION BY partition_col ORDER BY order_col
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS LAST_VAL
    FROM demo1
    ORDER BY partition_col, i, order_col;