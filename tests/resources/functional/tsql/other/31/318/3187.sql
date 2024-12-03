--Query type: DML
CREATE TABLE Employee
(
    EmployeeID INT,
    VacationHours INT
);

INSERT INTO Employee (EmployeeID, VacationHours)
VALUES
    (1, 10),
    (2, 20),
    (3, 30),
    (4, 40),
    (5, 50),
    (6, 60),
    (7, 70),
    (8, 80),
    (9, 90),
    (10, 100);

WITH TopEmployees AS
(
    SELECT TOP (10) EmployeeID, VacationHours
    FROM Employee
)
UPDATE TopEmployees
SET VacationHours = VacationHours * 1.25;

SELECT * FROM Employee;

-- REMORPH CLEANUP: DROP TABLE Employee;
