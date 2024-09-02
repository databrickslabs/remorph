--Query type: DML
DECLARE @Manager HIERARCHYID, @Child1 HIERARCHYID, @Child2 HIERARCHYID;
SET @Manager = CAST('/3/1/' AS HIERARCHYID);
SET @Child1 = CAST('/3/1/1/' AS HIERARCHYID);
SET @Child2 = CAST('/3/1/2/' AS HIERARCHYID);
WITH EmployeeCTE AS (
    SELECT @Manager.GetDescendant(@Child1, @Child2) AS OrgNode,
           'adventure-works\ThirdNewEmployee' AS LoginID,
           'Application Intern' AS Title,
           '3/11/07' AS HireDate
)
INSERT INTO HumanResources.EmployeeDemo (OrgNode, LoginID, Title, HireDate)
SELECT OrgNode, LoginID, Title, HireDate
FROM EmployeeCTE;