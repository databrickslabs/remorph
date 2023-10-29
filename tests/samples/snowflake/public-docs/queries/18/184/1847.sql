-- see https://docs.snowflake.com/en/sql-reference/functions/is-distinct-from

SELECT x1.i x1_i, x2.i x2_i,
               x1.i IS NOT DISTINCT FROM x2.i, iff(x1.i IS NOT DISTINCT FROM x2.i, 'Selected', 'Not') "SELECT IF X1.I IS NOT DISTINCT FROM X2.I",
               x1.i IS DISTINCT FROM x2.i, iff(x1.i IS DISTINCT FROM x2.i, 'Selected', 'Not') "SELECT IF X1.I IS DISTINCT FROM X2.I"
        FROM x x1, x x2
        ORDER BY x1.i, x2.i;