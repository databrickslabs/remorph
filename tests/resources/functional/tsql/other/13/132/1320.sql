-- tsql sql:
WITH customer_table AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 1 AS c_nationkey
    UNION ALL
    SELECT 2 AS c_custkey, 'Customer2' AS c_name, 2 AS c_nationkey
    UNION ALL
    SELECT 3 AS c_custkey, 'Customer3' AS c_name, 3 AS c_nationkey
)
SELECT c_custkey AS customer_key, c_name AS customer_name, c_nationkey AS nation_key
INTO myNewTable
FROM customer_table;

SELECT * FROM myNewTable;
-- REMORPH CLEANUP: DROP TABLE myNewTable;
