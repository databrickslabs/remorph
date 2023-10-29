-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showmaterializedviewoverhead-transact-sql?view=azure-sqldw-latest

DECLARE @p INT;
SELECT @p = 1;
WHILE (@p < 101)
BEGIN
    UPDATE t1 SET c1 = 1 WHERE c1 = 1;
    SELECT @p = @p + 1;
END;