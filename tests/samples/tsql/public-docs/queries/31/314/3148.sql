-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql-identity-property?view=sql-server-ver16

USE AdventureWorks2022;
GO
IF OBJECT_ID('dbo.new_employees', 'U') IS NOT NULL
    DROP TABLE new_employees;
GO

CREATE TABLE new_employees (
    id_num INT IDENTITY(1, 1),
    fname VARCHAR(20),
    minit CHAR(1),
    lname VARCHAR(30)
);

INSERT new_employees (fname, minit, lname)
VALUES ('Karin', 'F', 'Josephs');

INSERT new_employees (fname, minit, lname)
VALUES ('Pirkko', 'O', 'Koskitalo');