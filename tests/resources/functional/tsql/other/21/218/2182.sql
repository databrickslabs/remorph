--Query type: TCL
BEGIN TRANSACTION OuterTran2;
PRINT N'Transaction count after BEGIN OuterTran2 = ' + CAST(@@TRANCOUNT AS NVARCHAR(10));
INSERT INTO #TempTable (ID, Name)
SELECT ID, Name
FROM (
    VALUES (1, 'xxx'),
           (2, 'yyy'),
           (3, 'zzz')
) AS TempTable(ID, Name);
BEGIN TRANSACTION InnerTran1;
PRINT N'Transaction count after BEGIN InnerTran1 = ' + CAST(@@TRANCOUNT AS NVARCHAR(10));
INSERT INTO #TempTable (ID, Name)
SELECT ID, Name
FROM (
    VALUES (4, 'aaa'),
           (5, 'bbb'),
           (6, 'ccc')
) AS TempTable(ID, Name);
BEGIN TRANSACTION InnerTran2;
PRINT N'Transaction count after BEGIN InnerTran2 = ' + CAST(@@TRANCOUNT AS NVARCHAR(10));
INSERT INTO #TempTable (ID, Name)
SELECT ID, Name
FROM (
    VALUES (7, 'ddd'),
           (8, 'eee'),
           (9, 'fff')
) AS TempTable(ID, Name);
COMMIT TRANSACTION InnerTran2;
PRINT N'Transaction count after COMMIT InnerTran2 = ' + CAST(@@TRANCOUNT AS NVARCHAR(10));
COMMIT TRANSACTION InnerTran1;
PRINT N'Transaction count after COMMIT InnerTran1 = ' + CAST(@@TRANCOUNT AS NVARCHAR(10));
COMMIT TRANSACTION OuterTran2;
PRINT N'Transaction count after COMMIT OuterTran2 = ' + CAST(@@TRANCOUNT AS NVARCHAR(10));
