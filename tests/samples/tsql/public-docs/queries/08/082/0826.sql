-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/bulk-insert-transact-sql?view=sql-server-ver16

BULK INSERT Sales.Orders
FROM '\\SystemX\DiskZ\Sales\data\orders.dat';