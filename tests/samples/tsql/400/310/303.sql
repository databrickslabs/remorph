UPDATE OPENDATASOURCE('SQLNCLI', 'Data Source=<server name>;Integrated Security=SSPI').AdventureWorks2022.HumanResources.Department
SET GroupName = 'Sales and Marketing' WHERE DepartmentID = 4;