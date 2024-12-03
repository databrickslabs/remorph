--Query type: DQL
SELECT database_name, compatibility_level FROM (VALUES ('database1', 120), ('database2', 130)) AS databases (database_name, compatibility_level) WHERE database_name = 'database1';
