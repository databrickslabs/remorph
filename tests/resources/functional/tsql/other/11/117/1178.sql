-- tsql sql:
INSERT INTO #temp (col1, col2)
SELECT col1, col2
FROM (
    VALUES (1, 1), (2, 2)
) AS temp_result (col1, col2);

SELECT OBJECT_ID('tempdb.dbo.#temp') AS 'Object ID';
