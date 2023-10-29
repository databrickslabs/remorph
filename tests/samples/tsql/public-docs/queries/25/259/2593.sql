-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/table-transact-sql?view=sql-server-ver16

SELECT EmployeeID,
    DepartmentID
FROM @MyTableVar m
INNER JOIN Employee
    ON m.EmployeeID = Employee.EmployeeID
    AND m.DepartmentID = Employee.DepartmentID;