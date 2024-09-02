--Query type: DQL
SELECT T1.n_nationkey, T1.n_regionkey FROM (VALUES (1, 1), (2, 2), (3, 3)) AS T1 (n_nationkey, n_regionkey);