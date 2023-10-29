-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-object-permissions-transact-sql?view=sql-server-ver16

GRANT UNMASK ON OBJECT::Data.Membership (email) to OutreachCoordinator;
GO