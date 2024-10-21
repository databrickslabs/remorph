--Query type: DQL
WITH temp_result AS (SELECT DATABASEPROPERTYEX('tpch', 'IsFullTextEnabled') AS IsFullTextEnabled)
SELECT *
FROM temp_result;