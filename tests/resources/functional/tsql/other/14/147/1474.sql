--Query type: DML
DECLARE @Manager HIERARCHYID;
SET @Manager = CAST('/3/1/' AS HIERARCHYID);
INSERT INTO HumanResources.EmployeeDemo (OrgNode, LoginID, Title, HireDate)
SELECT *
FROM (
    VALUES (@Manager.GetDescendant(NULL, NULL), 'adventure-works\FirstNewEmployee', 'Application Intern', '2007-03-11')
) AS NewEmployee(OrgNode, LoginID, Title, HireDate);
