--Query type: DDL
WITH temp_result AS (
    SELECT 1 AS p_partkey, 'Part 1' AS p_name, 'Manufacturer 1' AS p_mfgr, 'Brand 1' AS p_brand, 'Type 1' AS p_type, 1 AS p_size, 'Container 1' AS p_container, 10.0 AS p_retailprice, 'Comment 1' AS p_comment
    UNION ALL
    SELECT 2, 'Part 2', 'Manufacturer 2', 'Brand 2', 'Type 2', 2, 'Container 2', 20.0, 'Comment 2'
    UNION ALL
    SELECT 3, 'Part 3', 'Manufacturer 3', 'Brand 3', 'Type 3', 3, 'Container 3', 30.0, 'Comment 3'
)
SELECT *
FROM temp_result;
