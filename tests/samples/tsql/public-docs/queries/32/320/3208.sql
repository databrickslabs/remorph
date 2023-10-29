-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-database-principal-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
DENY CONTROL ON USER::Wanida TO RolandX;  
GO