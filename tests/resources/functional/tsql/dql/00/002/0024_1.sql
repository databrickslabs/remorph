--Query type: DQL
SELECT * FROM (VALUES ('a', 1), ('b', 2), ('c', 3)) AS t2 (col1, col2) ORDER BY col1 COLLATE Latin1_General_CI_AS;