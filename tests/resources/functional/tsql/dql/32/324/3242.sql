--Query type: DQL
DECLARE @RowsToSkip TINYINT = 2, @FetchRows TINYINT = 8;

WITH TempResult AS (
    SELECT o_orderkey, o_custkey, o_orderstatus
    FROM (
        VALUES (1, 1, 'O'),
               (2, 2, 'O'),
               (3, 3, 'O'),
               (4, 4, 'O'),
               (5, 5, 'O'),
               (6, 6, 'O'),
               (7, 7, 'O'),
               (8, 8, 'O'),
               (9, 9, 'O'),
               (10, 10, 'O')
    ) AS Orders (o_orderkey, o_custkey, o_orderstatus)
)

SELECT o_orderkey, o_custkey, o_orderstatus
FROM TempResult
ORDER BY o_orderkey ASC
OFFSET @RowsToSkip ROWS
FETCH NEXT @FetchRows ROWS ONLY;