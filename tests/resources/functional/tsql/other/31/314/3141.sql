--Query type: DCL
DECLARE @sql nvarchar(max) = 'IF OBJECT_ID(''Purchasing.LowCredit'', ''TR'') IS NOT NULL
BEGIN
    DROP TRIGGER Purchasing.LowCredit;
END';
EXEC sp_executesql @sql;