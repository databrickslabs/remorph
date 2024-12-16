--
-- ORDER BY can have an optional OFFSET clause and FETCH clause.
-- Here we use some CTEs to try different variants that are allowed.
--
--

-- tsql sql:
WITH
    q1 AS (
        SELECT *
        FROM a_table
        ORDER BY 1
        OFFSET 0 ROWS FETCH FIRST 10 ROWS ONLY
    ),
    q2 AS (
        SELECT *
        from b_table
        ORDER BY 1 DESC
        OFFSET 1 ROW FETCH NEXT 1 ROW ONLY
    )

SELECT * FROM q1
UNION ALL
SELECT * FROM q2

ORDER BY 1;

-- databricks sql:
WITH
    q1 AS (
        SELECT *
        FROM a_table
        ORDER BY 1
        LIMIT 10 OFFSET 0
    ),
    q2 AS (
        SELECT *
        from b_table
        ORDER BY 1 DESC
        LIMIT 1 OFFSET 1
    )

(SELECT * FROM q1)
UNION ALL
(SELECT * FROM q2)

ORDER BY 1;
