
-- source:
select charindex('an', 'banana', 3),
                charindex('ab', 'abababab'), n, h, CHARINDEX(n, h) FROM pos;

-- databricks_sql:
SELECT CHARINDEX('an', 'banana', 3), CHARINDEX('ab', 'abababab'), n, h, CHARINDEX(n, h) FROM pos;
