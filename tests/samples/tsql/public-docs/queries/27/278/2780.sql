-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sid-transact-sql?view=sql-server-ver16

SELECT SUSER_SNAME(SUSER_SID('TestComputer\User', 0));