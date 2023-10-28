EXEC sp_create_plan_guide
    @name = N'Guide6',
    @stmt = N'SELECT c.LastName, c.FirstName, e.Title
              FROM HumanResources.Employee AS e
                   WITH (NOLOCK, INDEX (PK_Employee_EmployeeID))
              JOIN Person.Contact AS c ON e.ContactID = c.ContactID
              WHERE e.ManagerID = 3;',
    @type = N'SQL',
    @module_or_batch = NULL,
    @params = NULL,
    @hints = N'OPTION (TABLE HINT (e, INDEX(IX_Employee_ManagerID), NOLOCK, FORCESEEK))';
GO