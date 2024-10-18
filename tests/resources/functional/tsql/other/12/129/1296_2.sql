--Query type: DML
CREATE TABLE #employee_example
(
    employee_id INT,
    employee_name VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO #employee_example (employee_id, employee_name, salary)
VALUES
    (1, 'John Doe', 90000),
    (2, 'Jane Smith', 110000),
    (3, 'Bob Johnson', 120000);

SELECT *
FROM #employee_example
WHERE salary < 100000;

-- REMORPH CLEANUP: DROP TABLE #employee_example;