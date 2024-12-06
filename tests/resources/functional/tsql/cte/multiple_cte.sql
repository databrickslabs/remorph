--
-- Verify a few CTEs that include multiple expressions.
--

-- tsql sql:
WITH a AS (SELECT 1, 2, 3),
     b AS (SELECT 4, 5, 6),
     c AS (SELECT * FROM a)
SELECT * from b
UNION
SELECT * FROM c;

-- databricks sql:
WITH a AS (SELECT 1, 2, 3),
     b AS (SELECT 4, 5, 6),
     c AS (SELECT * FROM a)
(SELECT * from b)
UNION
(SELECT * FROM c);
