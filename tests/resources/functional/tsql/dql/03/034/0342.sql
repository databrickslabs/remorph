-- tsql sql:
DBCC CHECKDB();
SELECT *
FROM (
    VALUES ('DBCC CHECKDB()')
) AS temp_result_set(query);