-- tsql sql:
WITH MessageTypeCTE AS (
    SELECT 'InvoiceImage' AS MessageType, 'NONE' AS Validation
)
SELECT *
FROM MessageTypeCTE;