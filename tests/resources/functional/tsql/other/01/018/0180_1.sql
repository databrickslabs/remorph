-- tsql sql:
SELECT *
INTO #temp_table
FROM (
    VALUES ('value1', 'value2', 'value3', 'value4'),
           ('value5', 'value6', 'value7', 'value8')
) AS temp_table (c1, c2, c3, c4);

ALTER TABLE #temp_table
ALTER COLUMN c4 VARCHAR(100);

SELECT *
FROM #temp_table;

-- REMORPH CLEANUP: DROP TABLE #temp_table;
