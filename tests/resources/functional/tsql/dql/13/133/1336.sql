-- tsql sql:
CREATE TABLE #temp_table (colA sql_variant, colB INT);
INSERT INTO #temp_table
VALUES (CAST(46279.1 AS decimal(8, 2)), 1689);
SELECT SQL_VARIANT_PROPERTY(colA, 'BaseType') AS 'Base Type',
       SQL_VARIANT_PROPERTY(colA, 'Precision') AS 'Precision',
       SQL_VARIANT_PROPERTY(colA, 'Scale') AS 'Scale'
FROM #temp_table
WHERE colB = 1689
