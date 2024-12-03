--Query type: DQL
SELECT TOP 1 p_partkey, p_name, p_mfgr FROM (VALUES (1, 'Part 1', 'Manufacturer 1'), (2, 'Part 2', 'Manufacturer 2'), (3, 'Part 3', 'Manufacturer 3')) AS p (p_partkey, p_name, p_mfgr) ORDER BY NEWID();
