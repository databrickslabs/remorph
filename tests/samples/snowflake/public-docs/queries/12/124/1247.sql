-- see https://docs.snowflake.com/en/sql-reference/operators-query

SELECT LastName, FirstName FROM employees
UNION ALL
SELECT FirstName AS LastName, LastName AS FirstName FROM contractors;