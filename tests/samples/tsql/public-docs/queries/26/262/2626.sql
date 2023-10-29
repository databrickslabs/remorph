-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/opendatasource-transact-sql?view=sql-server-ver16

SELECT GroupName, Name, DepartmentID  
FROM OPENDATASOURCE('MSOLEDBSQL', 'Server=Seattle1;Database=AdventureWorks2022;TrustServerCertificate=Yes;Trusted_Connection=Yes;').HumanResources.Department  
ORDER BY GroupName, Name;