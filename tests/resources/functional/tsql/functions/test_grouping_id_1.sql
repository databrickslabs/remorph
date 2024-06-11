-- ## GROUPING_ID
--
-- There is no direct equivalent of GROUPING_ID in Databricks SQL. The following suggested translation
-- will achieve the same effect, though there may be other approaches to this.
--
-- One such approach may be:
-- ```sql
-- SELECT (GROUPING(col1) << 1) + GROUPING(colb) AS grouping_id
-- FROM t1
-- GROUP BY col1, col2 WITH CUBE;
-- ```

-- tsql sql:
SELECT GROUPING_ID(col1, col2) FROM t1 GROUP BY CUBE(col1, col2);

-- databricks sql:
SELECT CASE
           WHEN GROUPING(col1) = 1 AND GROUPING(col2) = 1 THEN 3
           WHEN GROUPING(col1) = 1 THEN 1
           WHEN GROUPING(col2) = 1 THEN 2
           ELSE 0
           END AS GROUPING_ID
FROM t1
GROUP BY CUBE(col1, col2);
