-- tsql sql:
WITH temp_result AS (
    SELECT c_custkey, c_nationkey, c_acctbal, (
        SELECT MAX(c_acctbal)
        FROM customer
    ) AS max_acctbal, (
        SELECT MIN(c_acctbal)
        FROM customer
    ) AS min_acctbal
    FROM customer
)
SELECT c_custkey, c_nationkey, c_acctbal, CASE
    WHEN c_acctbal > max_acctbal THEN max_acctbal
    WHEN c_acctbal < min_acctbal THEN min_acctbal
    ELSE c_acctbal
END AS greatest
FROM temp_result
ORDER BY c_custkey;
