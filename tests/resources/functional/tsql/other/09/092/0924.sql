--Query type: DCL
DECLARE @ServerEdition VARCHAR(50) = 'Standard';
WITH EditionCheck AS (
    SELECT CASE WHEN @ServerEdition IN ('Enterprise', 'Developer') THEN 'Supported' ELSE 'Not Supported' END AS EditionSupport
)
SELECT EditionSupport, CASE WHEN EditionSupport = 'Supported' THEN 'ALTER DATABASE statement executed successfully.' ELSE 'ALTER DATABASE statement failed; this functionality is not available in the current edition of SQL Server.' END AS Outcome
FROM EditionCheck;