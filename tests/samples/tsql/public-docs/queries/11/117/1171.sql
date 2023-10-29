-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-statistics-transact-sql?view=sql-server-ver16

CREATE STATISTICS CustomerStatsSampleScan
ON DimCustomer (CustomerKey, EmailAddress) WITH SAMPLE 50 PERCENT;