-- tsql sql:
WITH EmployeeCTE AS ( SELECT * FROM ( VALUES ('John', 'Doe', '123 Main St'), ('Jane', 'Doe', '456 Elm St') ) AS Employee ( FirstName, LastName, Address ) ) SELECT * FROM EmployeeCTE AS e1 UNION SELECT * FROM EmployeeCTE AS e2 OPTION ( MERGE UNION );
