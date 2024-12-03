--Query type: DQL
SELECT p_partkey, p_name, p_mfgr
FROM (
    VALUES
        (1, 'Part 1', 'Manufacturer 1'),
        (2, 'Part 2', 'Manufacturer 2')
) p (p_partkey, p_name, p_mfgr)
WHERE EXISTS (
    SELECT *
    FROM STRING_SPLIT('Manufacturer 1,Manufacturer 2', ',')
    WHERE value IN ('Manufacturer 1', 'Manufacturer 2')
)
