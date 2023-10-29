-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16

ALTER TABLE table1
ADD CONSTRAINT PK_Constrain PRIMARY KEY CLUSTERED (a)
WITH (ONLINE = ON, MAXDOP = 2, RESUMABLE = ON, MAX_DURATION = 240);