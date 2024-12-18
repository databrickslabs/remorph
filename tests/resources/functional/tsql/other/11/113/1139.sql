-- tsql sql:
WITH EmployeeList AS ( SELECT * FROM ( VALUES (1, 'John', 'Doe'), (2, 'Jane', 'Doe') ) AS EmployeeList ( Id, FirstName, LastName ) ) SELECT * FROM EmployeeList WHERE Id = 1
