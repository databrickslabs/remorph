-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver16

CREATE DATABASE MyLedgerDB ( EDITION = 'GeneralPurpose' ) WITH LEDGER = ON;
GO

CREATE SCHEMA [HR];
GO

CREATE TABLE [HR].[Employees]
(
    EmployeeID INT NOT NULL,
    Salary Money NOT NULL
)
GO