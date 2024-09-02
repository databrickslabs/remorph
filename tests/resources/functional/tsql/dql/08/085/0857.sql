--Query type: DQL
SELECT p_partkey FROM (VALUES (1, 'Part1'), (2, 'Part2')) AS part_table (p_partkey, p_name);