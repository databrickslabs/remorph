--Query type: DCL
CREATE TABLE #temp_result (Name VARCHAR(50), Address VARCHAR(50));
INSERT INTO #temp_result (Name, Address)
VALUES ('Customer1', 'Address1'), ('Customer2', 'Address2');
GRANT SELECT ON #temp_result TO MarketingTeam WITH GRANT OPTION;
SELECT * FROM #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;
