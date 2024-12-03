--Query type: DQL
WITH objects AS ( SELECT 'table' AS type, 'customer' AS name, 'public' AS schema_id ), columns AS ( SELECT 'column' AS type, 'c_custkey' AS name, 'customer' AS table_name ), database_files AS ( SELECT 'file' AS type, 'tpch.db' AS name, 'public' AS schema_id ) SELECT * FROM objects UNION ALL SELECT * FROM columns UNION ALL SELECT * FROM database_files
