-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/isdescendantof-database-engine?view=sql-server-ver16

DECLARE @Manager hierarchyid  
SELECT @Manager = OrgNode FROM HumanResources.EmployeeDemo  
  WHERE LoginID = 'adventure-works\dylan0'  
  
SELECT * FROM HumanResources.EmployeeDemo  
WHERE OrgNode.IsDescendantOf(@Manager) = 1