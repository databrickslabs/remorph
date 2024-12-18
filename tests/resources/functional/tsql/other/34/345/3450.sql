-- tsql sql:
CREATE TABLE #Customer (ID INT, Name VARCHAR(255));
CREATE TABLE #MarketingTeam (TeamName VARCHAR(255));
INSERT INTO #MarketingTeam (TeamName) VALUES ('MarketingTeam');
REVOKE SELECT ON #Customer FROM public;
WITH CustomerCTE AS (
    SELECT ID, Name FROM #Customer
)
SELECT * FROM CustomerCTE;
DROP TABLE #Customer;
DROP TABLE #MarketingTeam;
-- REMORPH CLEANUP: DROP TABLE #Customer;
-- REMORPH CLEANUP: DROP TABLE #MarketingTeam;
