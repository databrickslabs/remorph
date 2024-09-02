--Query type: DQL
DECLARE @StartingRowNumber TINYINT = 1, @EndingRowNumber TINYINT = 8;

WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_nationkey
    FROM (
        VALUES (1, 'Customer#1', 1),
               (2, 'Customer#2', 2),
               (3, 'Customer#3', 3),
               (4, 'Customer#4', 4),
               (5, 'Customer#5', 5),
               (6, 'Customer#6', 6),
               (7, 'Customer#7', 7),
               (8, 'Customer#8', 8)
    ) AS Customer(c_custkey, c_name, c_nationkey)
)

SELECT c_custkey, c_name, c_nationkey
FROM CustomerCTE
ORDER BY c_custkey ASC
OFFSET @StartingRowNumber - 1 ROWS
FETCH NEXT @EndingRowNumber - @StartingRowNumber + 1 ROWS ONLY
OPTION (OPTIMIZE FOR (@StartingRowNumber = 1, @EndingRowNumber = 20));