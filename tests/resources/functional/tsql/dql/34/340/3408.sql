--Query type: DQL
WITH EmployeePayHistory AS ( SELECT 1 AS BusinessEntityID, '2022-01-01' AS RateChangeDate, 10.00 AS Rate ) SELECT * FROM EmployeePayHistory;