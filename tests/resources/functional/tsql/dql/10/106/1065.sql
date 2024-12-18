-- tsql sql:
DECLARE @param INT = 10;
SELECT $PARTITION.RangePF1(id)
FROM (
    VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)
) AS T(id);
