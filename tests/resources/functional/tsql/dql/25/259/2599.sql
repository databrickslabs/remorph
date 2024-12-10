-- tsql sql:
SELECT t.filegroup_id, t.filegroup_name AS [Filegroup ID]
FROM (
    VALUES (1, 'PRIMARY'),
           (2, 'SECONDARY')
) t (filegroup_id, filegroup_name);
