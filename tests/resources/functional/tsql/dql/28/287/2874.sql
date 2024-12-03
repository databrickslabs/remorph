--Query type: DQL
WITH temp_result AS (SELECT n_nationkey, n_name FROM (VALUES (1, 'Nation1'), (2, 'Nation2')) AS t (n_nationkey, n_name)) SELECT n_nationkey, n_name FROM temp_result WHERE $PARTITION.RangePFNation(n_nationkey) = 2;
