-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/newsequentialid-transact-sql?view=sql-server-ver16

CREATE TABLE myTable (ColumnA uniqueidentifier DEFAULT NEWSEQUENTIALID());