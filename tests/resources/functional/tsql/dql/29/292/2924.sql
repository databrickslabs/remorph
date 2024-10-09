--Query type: DQL
WITH temp_result AS (SELECT 'file1' AS name, 'file1.phys' AS physical_name, 1 AS database_id
UNION ALL
SELECT 'file2', 'file2.phys', 2)
SELECT name, physical_name
FROM temp_result
WHERE database_id = (SELECT DB_ID('tpch_database'))