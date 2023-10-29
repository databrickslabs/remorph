-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sname-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

CREATE TABLE sname_example (
    login_sname SYSNAME DEFAULT SUSER_SNAME(),
    employee_id UNIQUEIDENTIFIER DEFAULT NEWID(),
    login_date DATETIME DEFAULT GETDATE()
    );
GO

INSERT sname_example DEFAULT
VALUES;
GO