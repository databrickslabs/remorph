--Query type: DML
CREATE TABLE #tempResult (Employee_LastName VARCHAR(50));
INSERT INTO #tempResult (Employee_LastName)
VALUES ('Smith'), ('Johnson'), ('Williams'), ('Jones'), ('Brown');

CREATE STATISTICS Employee_LastName_Stats ON #tempResult (Employee_LastName);
UPDATE STATISTICS #tempResult (Employee_LastName_Stats);

SELECT * FROM #tempResult;

-- REMORPH CLEANUP: DROP TABLE #tempResult;