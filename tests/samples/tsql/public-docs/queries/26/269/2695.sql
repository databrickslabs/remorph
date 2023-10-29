-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/tostring-database-engine?view=sql-server-ver16

SELECT OrgNode,  
OrgNode.ToString() AS Node  
FROM HumanResources.EmployeeDemo  
ORDER BY OrgNode ;  
GO