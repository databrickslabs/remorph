EXEC sp_create_plan_guide
    @name = N'Guide3',
    @stmt = N'SELECT c.LastName, c.FirstName, HumanResources.Employee.Title
              FROM HumanResources.Employee
              JOIN Person.Contact AS c ON HumanResources.Employee.ContactID = c.ContactID
              WHERE HumanResources.Employee.ManagerID = 3
              ORDER BY c.LastName, c.FirstName;',
    @type = N'SQL',
    @module_or_batch = NULL,
    @params = NULL,
    @hints = N'OPTION (TABLE HINT( HumanResources.Employee, FORCESEEK))';
GO