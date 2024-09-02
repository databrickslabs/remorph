--Query type: DQL
DECLARE @db_id INT, @object_id INT;

WITH temp_result AS (
    SELECT 1 AS db_id, 2 AS object_id
)

SELECT @db_id = db_id, @object_id = object_id
FROM temp_result;

SELECT ius.alloc_unit_type_desc, ius.page_count, ius.avg_page_space_used_in_percent, ius.record_count
FROM sys.dm_db_index_physical_stats(@db_id, @object_id, NULL, NULL, 'Detailed') AS ius;