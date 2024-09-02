--Query type: DDL
CREATE TABLE t7 (suppkey INT, name VARCHAR(255));
SELECT *
FROM (
    VALUES (1, 'a'),
           (2, 'b')
) AS supplier (suppkey, name)
WHERE suppkey > 1
      AND name IN ('a', 'b');