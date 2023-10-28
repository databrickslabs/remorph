SELECT department_id
FROM employees
GROUP BY department_id
HAVING count(*) < 10;