-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/rowversion-transact-sql?view=sql-server-ver16

CREATE TABLE ExampleTable2 (PriKey int PRIMARY KEY, VerCol rowversion) ;