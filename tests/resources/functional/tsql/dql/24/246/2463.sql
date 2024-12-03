--Query type: DQL
WITH temp_result AS (SELECT 'SQL_Latin1_General_CP1_CI_AS' AS collation_name)
SELECT COLLATIONPROPERTY(collation_name, 'CodePage')
FROM temp_result;
