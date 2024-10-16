--Query type: DQL
WITH temp_result AS (SELECT 'datetime' AS type_name)
SELECT TYPE_NAME(TYPE_ID(type_name)) AS [TYPE_NAME_ALIAS], TYPE_ID(type_name) AS [TYPE_ID_ALIAS]
FROM temp_result;