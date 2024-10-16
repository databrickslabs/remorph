--Query type: DQL
SELECT T1.n_name, T1.n_nationkey FROM (VALUES ('ALGERIA', 0), ('ARGENTINA', 1), ('BRAZIL', 2)) AS T1 (n_name, n_nationkey);