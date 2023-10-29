-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/getroot-database-engine?view=sql-server-ver16

SELECT OrgNode.ToString() AS Text_OrgNode, *  
FROM HumanResources.EmployeeDemo  
WHERE OrgNode = hierarchyid::GetRoot()