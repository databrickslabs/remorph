-- tsql sql:
SELECT emp_id, emp_name, hourly_wage, salary, commission, num_sales
INTO #employee_wages
FROM (
    VALUES (1, 'John', 10.0, 50000.0, 1000.0, 10)
) AS temp (emp_id, emp_name, hourly_wage, salary, commission, num_sales);

SELECT *
FROM #employee_wages;

-- REMORPH CLEANUP: DROP TABLE #employee_wages;
