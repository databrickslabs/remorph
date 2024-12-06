-- tsql sql:
WITH CustomerCTE AS (SELECT 'Smith' AS LastName, 'John' AS FirstName, 'Sales' AS JobTitle), EmployeeCTE AS (SELECT 'Johnson' AS LastName, 'Mike' AS FirstName, 'Manager' AS JobTitle) SELECT c.LastName, c.FirstName, e.JobTitle FROM CustomerCTE AS c WITH (INDEX = 0) JOIN EmployeeCTE AS e ON c.LastName = e.LastName WHERE c.LastName = 'Smith';
