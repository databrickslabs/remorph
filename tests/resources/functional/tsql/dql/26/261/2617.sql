-- tsql sql:
WITH CustomerCTE AS (
    SELECT c_name, REVERSE(c_name) AS ReverseName
    FROM (
        VALUES ('Customer#000000001'),
               ('Customer#000000002'),
               ('Customer#000000003'),
               ('Customer#000000004'),
               ('Customer#000000005')
    ) AS Customer(c_name)
)
SELECT c_name, ReverseName
FROM CustomerCTE
WHERE c_name < 'Customer#000000005'
ORDER BY c_name;
