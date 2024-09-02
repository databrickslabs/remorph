--Query type: DDL
SELECT * FROM (VALUES (1, 'John', 'Doe'), (2, 'Jane', 'Doe')) AS EmployeesCTE (Id, FirstName, LastName) WHERE Id = 1;