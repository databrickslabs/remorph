-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/exp-transact-sql?view=sql-server-ver16

SELECT EXP(LOG(20)), LOG(EXP(20))  
GO