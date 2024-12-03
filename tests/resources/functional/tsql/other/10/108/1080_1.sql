--Query type: DML
DECLARE @RowCount INT;
DECLARE @Balance DECIMAL(10, 2) = 1000.00;
DECLARE @sql NVARCHAR(MAX) = 'SELECT @RowCount = COUNT(*) FROM (VALUES (1), (2), (3)) AS TempTable';
EXEC sp_executesql @sql, N'@RowCount INT OUTPUT', @RowCount OUTPUT;
PRINT @RowCount;
