--Query type: DQL
SELECT p_partkey, p_name, p_mfgr
FROM (
    VALUES
        (1, 'part1', 'mfgr1, mfgr2'),
        (2, 'part2', 'mfgr3, mfgr4')
) AS p (p_partkey, p_name, p_mfgr)
WHERE 'mfgr1' IN (
    SELECT value
    FROM STRING_SPLIT(p.p_mfgr, ',')
);