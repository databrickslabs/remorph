-- tsql sql:
DECLARE @AuditState nvarchar(10);

WITH AuditStateCTE AS (
    SELECT 'OFF' AS State
)

SELECT @AuditState = State FROM AuditStateCTE;

DECLARE @sql nvarchar(max) = N'ALTER SERVER AUDIT PCI_Audit WITH (STATE = ' + @AuditState + ');';

EXEC sp_executesql @sql;
