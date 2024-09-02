--Query type: DCL
CREATE TABLE HumanResources.Employee
(
    EmployeeID INT,
    EmployeeName VARCHAR(255),
    HireDate DATE
);

INSERT INTO HumanResources.Employee (EmployeeID, EmployeeName, HireDate)
VALUES
    (1, 'Employee1', '2022-01-01'),
    (2, 'Employee2', '2022-01-15');

WITH employee AS
(
    SELECT EmployeeID, EmployeeName, HireDate
    FROM HumanResources.Employee
)
SELECT *
FROM employee;
-- REMORPH CLEANUP: DROP TABLE HumanResources.Employee;