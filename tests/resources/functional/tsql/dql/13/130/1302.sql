--Query type: DQL
WITH temp_result AS (
  SELECT 'customer' AS type, 'John' AS name, 25 AS age
  UNION ALL
  SELECT 'customer' AS type, 'Jane' AS name, 30 AS age
  UNION ALL
  SELECT 'employee' AS type, 'Bob' AS name, 35 AS age
)
SELECT type, AVG(age) AS average_age
FROM temp_result
WHERE type = 'customer'
GROUP BY type
HAVING AVG(age) > 20
