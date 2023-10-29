-- see https://docs.snowflake.com/en/sql-reference/functions/equal_null

SELECT x1.i x1_i, 
       x2.i x2_i,
       equal_null(x1.i,x2.i), 
       iff(equal_null(x1.i,x2.i), 'Selected', 'Not') "SELECT IF EQUAL_NULL(X1.I,X2.I)",
       not(equal_null(x1.i,x2.i)), 
       iff(not(equal_null(x1.i,x2.i)), 'Selected', 'Not') "SELECT IF NOT(EQUAL_NULL(X1.I,X2.I))"
    FROM x x1, x x2;