-- tsql sql:
WITH temp_sql_modules AS (
    SELECT 'definition1' AS definition, 'type1' AS type, 1 AS object_id
),
 temp_objects AS (
    SELECT 'name1' AS name, 'type1' AS type, 1 AS object_id
)
SELECT tsm.definition, tos.type
FROM temp_sql_modules AS tsm
JOIN temp_objects AS tos ON tsm.object_id = tos.object_id AND tos.type IN ('FN', 'IF', 'TF');
