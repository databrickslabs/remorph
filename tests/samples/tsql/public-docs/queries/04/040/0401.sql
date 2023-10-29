-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-set-options?view=sql-server-ver16

--Connect to [database_name];
GO
ALTER DATABASE [database_name]
SET RESTRICTED_USER;
GO
ALTER DATABASE [database_name]
SET READ_ONLY
--`SET READ_ONLY` command may take a few seconds to complete.
GO
ALTER DATABASE [database_name]
SET MULTI_USER;
GO