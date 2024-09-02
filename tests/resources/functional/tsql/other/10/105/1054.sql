--Query type: DDL
WITH MessageTypeCTE AS (
    SELECT 'Example-Company.com/Orders/SubmitOrder' AS MessageType, 'EMPTY' AS Validation
)
SELECT *
FROM MessageTypeCTE;
-- REMORPH CLEANUP: No objects were created in this query.