--Query type: DQL
WITH temp_result AS ( SELECT 'datetime' AS type_name ) SELECT TYPE_NAME(TYPE_ID(type_name)) AS typeName, TYPE_ID(type_name) AS typeID FROM temp_result;