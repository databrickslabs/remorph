--Query type: DML
DECLARE @MyBinVar varbinary(128);
SET @MyBinVar = CAST(REPLICATE(0x30, 128) AS varbinary(128));
SET CONTEXT_INFO @MyBinVar;
WITH MyCTE AS (
    SELECT CONTEXT_INFO() AS MyNewContextInfo
)
SELECT * FROM MyCTE;