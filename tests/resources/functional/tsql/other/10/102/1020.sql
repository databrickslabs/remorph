--Query type: DDL
CREATE TABLE #Customer (c_nationkey INT, c_acctbal DECIMAL(10, 2));
INSERT INTO #Customer (c_nationkey, c_acctbal)
VALUES (1, 100.0), (2, 200.0), (3, 300.0);
CREATE INDEX IX_CN ON #Customer (c_nationkey ASC, c_acctbal ASC);
SELECT * FROM #Customer;
-- REMORPH CLEANUP: DROP INDEX IX_CN ON #Customer;
-- REMORPH CLEANUP: DROP TABLE #Customer;