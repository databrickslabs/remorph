--Query type: DML
DECLARE @waittimesec INT = 2;
DECLARE @startingtime DATETIME2(2) = GETDATE();
PRINT N'Waiting for ' + CAST(@waittimesec AS VARCHAR(5)) + ' seconds';
WHILE (1 = 1)
BEGIN
    PRINT N'Waiting.';
    IF DATEDIFF(s, GETDATE(), @startingtime) > @waittimesec
    BEGIN
        PRINT 'We have finished waiting.';
        BREAK;
    END
END