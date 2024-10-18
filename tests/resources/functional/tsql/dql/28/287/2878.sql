--Query type: DQL
SELECT d.* FROM (VALUES ('Sales', 100), ('Marketing', 200), ('IT', 300)) AS d (DepartmentName, DepartmentID);