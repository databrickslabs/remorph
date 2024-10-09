--Query type: DDL
CREATE TABLE #Temp (i INT, x XML);

WITH CTE AS (
    SELECT 1 AS i, '<root><element>value</element></root>' AS x
)

SELECT i, x.value('(//element)[1]', 'varchar(50)') AS element_value
FROM CTE;

SELECT * FROM #Temp;

-- REMORPH CLEANUP: DROP TABLE #Temp;