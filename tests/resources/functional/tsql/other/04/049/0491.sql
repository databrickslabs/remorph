-- tsql sql:
CREATE TABLE #AvailabilityGroups (AvailabilityGroupName sysname, REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT int);
INSERT INTO #AvailabilityGroups (AvailabilityGroupName, REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT)
VALUES ('AG_TPC_H', 3);
SELECT * FROM #AvailabilityGroups;
-- REMORPH CLEANUP: DROP TABLE #AvailabilityGroups;
