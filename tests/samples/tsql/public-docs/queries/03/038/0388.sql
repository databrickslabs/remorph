-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-as-clone-of-transact-sql?view=fabric

--Clone creation across schemas
CREATE TABLE dbo.Employee AS CLONE OF dbo1.EmployeeUSA;