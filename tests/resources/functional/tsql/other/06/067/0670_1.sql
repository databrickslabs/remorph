--Query type: DML
CREATE TABLE department (department_ID INT, department_name VARCHAR(50));
WITH department_CTE AS (
    SELECT *
    FROM (
        VALUES (1, 'Sales'),
               (2, 'Marketing'),
               (3, 'IT')
    ) AS department (department_ID, department_name)
)
INSERT INTO department (department_ID, department_name)
SELECT department_ID, department_name
FROM department_CTE;
SELECT *
FROM department;