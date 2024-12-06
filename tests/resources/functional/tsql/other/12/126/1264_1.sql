-- tsql sql:
DECLARE @EmployeeVar TABLE (EmployeeID INT NOT NULL, EmployeeName NVARCHAR(50) NOT NULL, Salary MONEY NOT NULL);

WITH EmployeeCTE AS (
    SELECT EmployeeID, EmployeeName, Salary
    FROM (
        VALUES (1, 'John Doe', 50000.00),
               (2, 'Jane Doe', 60000.00),
               (3, 'Bob Smith', 70000.00)
    ) AS Employee (EmployeeID, EmployeeName, Salary)
)

SELECT EmployeeID, EmployeeName, Salary
FROM EmployeeCTE
WHERE Salary > 55000.00;
