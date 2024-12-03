--Query type: DQL
SELECT c_custkey, c_name, c_nationkey
FROM (
    VALUES
        (1, 'Customer1', 1),
        (2, 'Customer2', 2),
        (3, 'Customer3', 3),
        (4, 'Customer4', 4),
        (5, 'Customer5', 5),
        (6, 'Customer6', 6),
        (7, 'Customer7', 7),
        (8, 'Customer8', 8),
        (9, 'Customer9', 9),
        (10, 'Customer10', 10)
) AS Customer (c_custkey, c_name, c_nationkey)
ORDER BY c_custkey
OFFSET 5 ROWS;
