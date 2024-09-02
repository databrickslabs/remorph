--Query type: DML
INSERT INTO #TempResult (Column1, Column2)
SELECT Column1, Column2
FROM (
    VALUES (1, 10.0),
           (1, 20.0)
) AS TempTable (Column1, Column2);