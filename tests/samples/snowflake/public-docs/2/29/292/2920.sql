SELECT LastName, FirstName FROM employees
UNION ALL
SELECT FirstName, LastName FROM contractors;