--Query type: DCL
DECLARE customer_cursor CURSOR FOR
    SELECT c.name, o.order_id
    FROM (
        VALUES ('Customer1', 1),
               ('Customer2', 2),
               ('Customer3', 3)
    ) AS c (name, customer_id)
    JOIN (
        VALUES (1, 100),
               (2, 200),
               (3, 300)
    ) AS o (customer_id, order_id)
        ON c.customer_id = o.customer_id
    WHERE c.name = 'Customer1';