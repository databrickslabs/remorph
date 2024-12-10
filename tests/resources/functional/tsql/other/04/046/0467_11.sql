-- tsql sql:
DROP TABLE #TempTable;
SELECT *
FROM (
    VALUES (
        (1, 'John Doe'),
        (2, 'Jane Doe')
    )
) AS #TempTable (ID, Name);
