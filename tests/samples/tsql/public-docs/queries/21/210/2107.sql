-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table?view=sql-server-ver16

FROM t WITH (TABLOCK, INDEX(myindex))