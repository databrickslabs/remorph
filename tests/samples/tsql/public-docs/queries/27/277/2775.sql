-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sname-transact-sql?view=sql-server-ver16

SELECT SUSER_SNAME() AS CurrentLogin;
GO