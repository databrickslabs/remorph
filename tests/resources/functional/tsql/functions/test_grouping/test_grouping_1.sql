## GROUPING

The TSql GROUPING() function is directly equivalent in Databricks SQL. There are however
some differences that should be accounted for.

   - TSql supports GROUPING on column aliases, while Databricks SQL does not.
   - TSql allowe GROUPING to be used in GROUPING SETS, The GROUPING function in Databricks
     does not support GROUPING SETS
   - TSql returns a 1 or 0, wheras Databicks returns a boolean

-- tsql sql:
SELECT GROUPING(col1) FROM t1 GROUP BY col1 WITH ROLLUP;

-- databricks sql:
SELECT GROUPING(col1) FROM t1 GROUP BY col1 WITH ROLLUP;
