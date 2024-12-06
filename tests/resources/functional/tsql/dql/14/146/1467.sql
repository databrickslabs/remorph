-- tsql sql:
DECLARE @List AS nvarchar(max);
WITH CustomerCTE AS (
    SELECT c_name, c_custkey, c_nationkey
    FROM customer
)
SELECT @List = CONCAT(COALESCE(@List + ', ', ''), c_name)
FROM CustomerCTE
WHERE c_nationkey = 1
ORDER BY c_custkey;
SELECT @List;
