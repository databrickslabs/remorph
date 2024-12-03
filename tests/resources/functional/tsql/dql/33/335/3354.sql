--Query type: DQL
WITH temp_result AS (SELECT 'customer' AS table_name)
SELECT IDENT_SEED(table_name) AS Identity_Seed
FROM temp_result;
