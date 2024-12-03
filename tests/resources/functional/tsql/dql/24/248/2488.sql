--Query type: DQL
WITH EmployeeCTE AS ( SELECT * FROM ( VALUES (1, 'John'), (2, 'Jane'), (3, 'Bob') ) AS Employee (EmployeeID, Name) ) SELECT COUNT(*) FROM EmployeeCTE
