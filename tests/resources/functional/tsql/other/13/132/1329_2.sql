--Query type: DDL
WITH customer_temp AS (
    SELECT c_custkey, c_nationkey
    FROM (
        VALUES (1, 1), (2, 2)
    ) AS temp(c_custkey, c_nationkey)
)
SELECT *
INTO #customer_temp
FROM customer_temp;

CREATE NONCLUSTERED INDEX ix_custkey_nationkey
ON #customer_temp (c_custkey, c_nationkey);
