-- see https://docs.snowflake.com/en/sql-reference/functions/is-distinct-from

SELECT x1.i x1_i, x2.i x2_i 
    FROM x x1, x x2 
    WHERE x1.i=x2.i;