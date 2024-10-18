--Query type: DQL
SELECT *
FROM (
    VALUES
        (1, 'John', 'Manager'),
        (2, 'Alice', 'Employee'),
        (3, 'Bob', 'Employee')
) AS employee_hierarchy_02 (
    employee_ID,
    employee_name,
    employee_title
)
ORDER BY employee_ID;