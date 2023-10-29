-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/is-srvrolemember-transact-sql?view=sql-server-ver16

SELECT IS_SRVROLEMEMBER('diskadmin', 'Contoso\Pat');