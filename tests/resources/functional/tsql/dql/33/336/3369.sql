-- tsql sql:
SELECT p_partkey, p_mfgr, p_brand, NULLIF(p_mfgr, p_brand) AS [Null if Equal]
FROM (
    VALUES (1, 'MFGR#1', 'Brand#1'),
           (2, 'MFGR#2', 'Brand#2'),
           (3, 'MFGR#3', 'Brand#3'),
           (4, 'MFGR#4', 'Brand#4'),
           (5, 'MFGR#5', 'Brand#5'),
           (6, 'MFGR#6', 'Brand#6'),
           (7, 'MFGR#7', 'Brand#7'),
           (8, 'MFGR#8', 'Brand#8'),
           (9, 'MFGR#9', 'Brand#9')
) AS t (p_partkey, p_mfgr, p_brand)
WHERE p_partkey < 10;
