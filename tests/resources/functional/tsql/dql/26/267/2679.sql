--Query type: DQL
WITH SequenceCTE AS (
    SELECT 1 AS seq_value
    UNION ALL
    SELECT seq_value + 1
    FROM SequenceCTE
    WHERE seq_value < 100
)
SELECT NEXT VALUE FOR customer_total_value_seq AS seq_value
FROM SequenceCTE
OPTION (MAXRECURSION 0);