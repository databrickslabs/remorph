-- tsql sql:
ALTER INDEX IX_SalesOrderHeader_SalesOrderID
ON Sales.SalesOrderHeader
REBUILD PARTITION = 3
WITH (ONLINE = ON (WAIT_AT_LOW_PRIORITY (MAX_DURATION = 5 MINUTES, ABORT_AFTER_WAIT = SELF)));