--Query type: TCL
CREATE TABLE orders (
    o_orderkey INT,
    o_custkey INT,
    o_comment VARCHAR(50)
);

WITH temp_result AS (
    SELECT 1 AS i_col, 11 AS j_col, NULL AS v
    UNION ALL
    SELECT 2, 12, 'O'
    UNION ALL
    SELECT 3, 12, 'I'
)
INSERT INTO orders (o_orderkey, o_custkey, o_comment)
SELECT i_col, j_col, v
FROM temp_result;

SELECT * FROM orders;
-- REMORPH CLEANUP: DROP TABLE orders;
