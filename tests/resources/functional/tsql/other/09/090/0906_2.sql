-- tsql sql:
CREATE TABLE temp (DepartmentID INT, DepartmentName VARCHAR(50));
INSERT INTO temp (DepartmentID, DepartmentName)
SELECT *
FROM (VALUES (1, 'Sales'), (2, 'Marketing')) AS temp_result(DepartmentID, DepartmentName);
