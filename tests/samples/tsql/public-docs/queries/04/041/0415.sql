-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-statistics-transact-sql?view=sql-server-ver16

--Create statistics on an external table and use default sampling.
CREATE STATISTICS CustomerStats1 ON DimCustomer (CustomerKey, EmailAddress);
  
--Create statistics on an external table and scan all the rows
CREATE STATISTICS CustomerStats1 ON DimCustomer (CustomerKey, EmailAddress) WITH FULLSCAN;