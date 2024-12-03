--Query type: DQL
SELECT FILEGROUPPROPERTY('PRIMARY', 'IsDefault') AS [Default Filegroup] FROM (VALUES (1)) AS dummy_table(dummy_column);
