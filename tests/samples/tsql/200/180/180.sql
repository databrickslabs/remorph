EXEC sp_create_plan_guide
    @name = N'Guide1',
    @stmt = N'SELECT c.LastName, c.FirstName, e.Title
              FROM HumanResources.Employee AS e
              JOIN Person.Contact AS c ON e.ContactID = c.ContactID
              WHERE e.ManagerID = 2;',
    @type = N'SQL',
    @module_or_batch = NULL,
    @params = NULL,
    @hints = N'OPTION (TABLE HINT(e, INDEX (IX_Employee_ManagerID)))';
GO
EXEC sp_create_plan_guide
    @name = N'Guide2',
    @stmt = N'SELECT c.LastName, c.FirstName, e.Title
              FROM HumanResources.Employee AS e
              JOIN Person.Contact AS c ON e.ContactID = c.ContactID
              WHERE e.ManagerID = 2;',
    @type = N'SQL',
    @module_or_batch = NULL,
    @params = NULL,
    @hints = N'OPTION (TABLE HINT(e, INDEX(PK_Employee_EmployeeID, IX_Employee_ManagerID)))';
GO