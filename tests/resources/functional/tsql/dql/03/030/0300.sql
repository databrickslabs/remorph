-- tsql sql:
WITH CustomerCTE AS (
    SELECT c_name, MIN(c_acctbal) AS MinimumAccountBalance
    FROM customer
    GROUP BY c_name
)
SELECT c_name, ISNULL(MinimumAccountBalance, 0) AS MinimumAccountBalance
FROM CustomerCTE
ORDER BY c_name;
