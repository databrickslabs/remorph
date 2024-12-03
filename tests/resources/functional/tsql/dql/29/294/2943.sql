--Query type: DQL
WITH temp_result AS (SELECT c_custkey, c_name FROM (VALUES (1, 'Customer1'), (2, 'Customer2'), (3, 'Customer3')) AS customer(c_custkey, c_name))
SELECT c_custkey, c_name
FROM temp_result
WHERE c_custkey BETWEEN 1 AND 3
    AND c_name LIKE 'Customer%';
