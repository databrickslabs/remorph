--Query type: DQL
SELECT n_name, n_nationkey FROM (VALUES ('name1', 1), ('name2', 2)) AS temp_result (n_name, n_nationkey);
