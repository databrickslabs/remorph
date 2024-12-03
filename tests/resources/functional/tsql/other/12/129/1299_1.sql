--Query type: DDL
SELECT id, name
INTO #temp_table
FROM (
    VALUES (1, 'name1'),
           (2, 'name2')
) AS temp_table(id, name);

ALTER TABLE #temp_table
ADD CONSTRAINT my_temp_constraint UNIQUE (id);

ALTER TABLE #temp_table
DROP CONSTRAINT my_temp_constraint;

SELECT *
FROM #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;
