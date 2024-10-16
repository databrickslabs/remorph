--Query type: DQL
WITH EmployeeCTE AS ( SELECT DISTINCT Title FROM ( VALUES ('Engineer'), ('Manager'), ('Analyst') ) AS Employee ( Title ) ) SELECT COUNT(DISTINCT Title) FROM EmployeeCTE