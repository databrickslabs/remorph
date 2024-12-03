--Query type: DQL
SELECT p_partkey, p_name FROM (VALUES (1, 'Part 1'), (2, 'Part 2')) AS p (p_partkey, p_name);
