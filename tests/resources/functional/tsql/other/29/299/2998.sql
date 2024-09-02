--Query type: DML
DECLARE @ContextInfo VARBINARY(128);
SELECT @ContextInfo = ContextInfo
FROM (
    VALUES (0x1256698456)
) AS ContextInfoTable(ContextInfo);
SET CONTEXT_INFO @ContextInfo;
SELECT CONTEXT_INFO();