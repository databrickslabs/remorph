-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sname-transact-sql?view=sql-server-ver16

SELECT SUSER_SNAME();
GO

EXECUTE AS LOGIN = 'WanidaBenShoof';
SELECT SUSER_SNAME();

REVERT;
GO

SELECT SUSER_SNAME();
GO