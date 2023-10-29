-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-as-clone-of-transact-sql?view=fabric

--Clone creation within the same schema
CREATE TABLE dbo.Employee AS CLONE OF dbo1.EmployeeUSA AT '2023-05-23T14:24:10';