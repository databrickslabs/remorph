--Query type: DQL
WITH temp_result AS (SELECT n_name, n_nationkey FROM customer)
SELECT n_name
FROM temp_result
WHERE n_nationkey = DB_ID()