--Query type: DQL
SELECT cn.c_name AS CustomerName
FROM (
    VALUES
        (1, 'Customer 1'),
        (2, 'Customer 2'),
        (3, 'Customer 3')
) cn (c_custkey, c_name)
INNER JOIN (
    VALUES
        (1),
        (2),
        (3)
) customer_ids (c_custkey)
    ON cn.c_custkey = customer_ids.c_custkey;
