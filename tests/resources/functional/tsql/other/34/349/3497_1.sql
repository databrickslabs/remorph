--Query type: DCL
CREATE TABLE #Audit
(
    AuditName nvarchar(50),
    State nvarchar(10),
    QueueDelay int
);

INSERT INTO #Audit (AuditName, State, QueueDelay)
VALUES ('PCI_Audit_New', 'OFF', 1000);

SELECT * FROM #Audit;

-- REMORPH CLEANUP: DROP TABLE #Audit;
