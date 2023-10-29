-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16

USE AdventureWorks;
ALTER TABLE Person.Person
ENABLE CHANGE_TRACKING ;