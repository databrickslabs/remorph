--Query type: DQL
WITH EmployeeCTE AS (
    SELECT nation_name, COUNT(employee_id) AS EmployeesInNation
    FROM (
        VALUES ('USA', 1),
               ('Canada', 2),
               ('Mexico', 3)
    ) AS T(nation_name, employee_id)
    GROUP BY nation_name
    HAVING COUNT(employee_id) > 1
)
SELECT nation_name, EmployeesInNation
FROM EmployeeCTE