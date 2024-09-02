--Query type: DCL
CREATE TABLE #T1 (cname sysname, c_id int);
INSERT INTO #T1 (cname, c_id)
VALUES ('customer', 1), ('orders', 2);

DBCC UPDATEUSAGE (#T1) WITH NO_INFOMSGS;

SELECT * FROM #T1;

-- REMORPH CLEANUP: DROP TABLE #T1;