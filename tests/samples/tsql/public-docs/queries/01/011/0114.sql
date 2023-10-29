-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/rename-transact-sql?view=aps-pdw-2016-au7

-- Rename the customer table
RENAME OBJECT Customer TO Customer1;

RENAME OBJECT mydb.dbo.Customer TO Customer1;