-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/getlevel-database-engine?view=sql-server-ver16

SELECT OrgNode.ToString() AS Text_OrgNode,   
OrgNode.GetLevel() AS EmpLevel, *  
FROM HumanResources.EmployeeDemo;