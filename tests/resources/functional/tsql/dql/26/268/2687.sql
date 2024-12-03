--Query type: DQL
WITH temp_result AS (
    SELECT c_custkey, c_nationkey
    FROM (
        VALUES (1, 1), (2, 2), (3, 3)
    ) AS customer(c_custkey, c_nationkey)
)
SELECT OBJECT_ID_FROM_EDGE_ID(CONVERT(nvarchar(50), c_custkey)) AS customer_id
FROM temp_result;
