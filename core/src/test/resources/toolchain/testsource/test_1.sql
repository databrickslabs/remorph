--
-- The use of CTEs is generally the same in Databricks SQL as TSQL but there are some differences with
-- nesting CTE support.
--
-- tsql sql:
WITH cte AS (SELECT * FROM t) SELECT * FROM cte
