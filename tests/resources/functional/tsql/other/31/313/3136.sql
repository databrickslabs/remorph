--Query type: DML
DECLARE @MyTableVar TABLE (BusinessEntityID INT, OldVacationHours INT, NewVacationHours INT, ModifiedDate DATETIME);
CREATE TABLE #EmployeeCTE (BusinessEntityID INT, VacationHours INT, ModifiedDate DATETIME);
INSERT INTO #EmployeeCTE (BusinessEntityID, VacationHours, ModifiedDate)
VALUES (1, 10, '2022-01-01'), (2, 20, '2022-01-02'), (3, 30, '2022-01-03'), (4, 40, '2022-01-04'), (5, 50, '2022-01-05'), (6, 60, '2022-01-06'), (7, 70, '2022-01-07'), (8, 80, '2022-01-08'), (9, 90, '2022-01-09'), (10, 100, '2022-01-10');
UPDATE TOP (10) #EmployeeCTE
SET VacationHours = VacationHours * 1.25
OUTPUT INSERTED.BusinessEntityID, DELETED.VacationHours, INSERTED.VacationHours, INSERTED.ModifiedDate
INTO @MyTableVar;
SELECT BusinessEntityID, OldVacationHours, NewVacationHours, ModifiedDate
FROM @MyTableVar;
-- REMORPH CLEANUP: DROP TABLE #EmployeeCTE;
