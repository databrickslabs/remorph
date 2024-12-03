--Query type: DDL
IF OBJECT_ID('tempdb..#TempTable', 'U') IS NOT NULL
BEGIN
    SELECT *
    FROM (
        VALUES (1)
    ) AS DerivedTable(Column1);
    DROP TABLE #TempTable;
END;
