--Query type: DML
DECLARE @stmt nvarchar(max) = N'
    WITH EmployeeCTE AS (
        SELECT 1 AS EmployeeID, ''John'' AS LastName, ''Doe'' AS FirstName, ''Manager'' AS Title, 1 AS ManagerID
        UNION ALL
        SELECT 2 AS EmployeeID, ''Jane'' AS LastName, ''Doe'' AS FirstName, ''Employee'' AS Title, 1 AS ManagerID
    ),
    ContactCTE AS (
        SELECT 1 AS ContactID, ''John'' AS LastName, ''Doe'' AS FirstName
        UNION ALL
        SELECT 2 AS ContactID, ''Jane'' AS LastName, ''Doe'' AS FirstName
    )
    SELECT e.LastName, e.FirstName, c.FirstName AS Title
    FROM EmployeeCTE AS e
    JOIN ContactCTE AS c ON e.EmployeeID = c.ContactID
    WHERE e.ManagerID = 1
    OPTION (TABLE HINT(e, FORCESEEK)) -- Modified hint for demonstration
';

EXEC sp_create_plan_guide
    @name = N'Guide3',
    @stmt = @stmt,
    @type = N'SQL',
    @module_or_batch = NULL,
    @params = NULL,
    @hints = N'OPTION (TABLE HINT(e, FORCESEEK))'; -- Modified hint for demonstration

-- Select data from the CTEs
WITH EmployeeCTE AS (
    SELECT 1 AS EmployeeID, 'John' AS LastName, 'Doe' AS FirstName, 'Manager' AS Title, 1 AS ManagerID
    UNION ALL
    SELECT 2 AS EmployeeID, 'Jane' AS LastName, 'Doe' AS FirstName, 'Employee' AS Title, 1 AS ManagerID
),
ContactCTE AS (
    SELECT 1 AS ContactID, 'John' AS LastName, 'Doe' AS FirstName
    UNION ALL
    SELECT 2 AS ContactID, 'Jane' AS LastName, 'Doe' AS FirstName
)
SELECT * FROM EmployeeCTE;
SELECT * FROM ContactCTE;

-- REMORPH CLEANUP: EXEC sp_control_plan_guide N'DROP', N'Guide3';