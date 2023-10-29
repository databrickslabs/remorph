-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-query?view=sql-server-ver16

EXEC sp_create_plan_guide
    @name = N'Guide5',
    @stmt = N'SELECT e.ManagerID, c.LastName, c.FirstName, e.Title
              FROM HumanResources.Employee AS e WITH (INDEX (IX_Employee_ManagerID))
              JOIN Person.Contact AS c ON e.ContactID = c.ContactID
              WHERE e.ManagerID = 3;',
    @type = N'SQL',
    @module_or_batch = NULL,
    @params = NULL,
    @hints = N'OPTION (TABLE HINT(e))';
GO