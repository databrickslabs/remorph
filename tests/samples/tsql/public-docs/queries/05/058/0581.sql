-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-index-transact-sql?view=sql-server-ver16

ALTER FULLTEXT INDEX ON Production.Document SET CHANGE_TRACKING AUTO;
GO