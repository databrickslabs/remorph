--Query type: TCL
BEGIN TRANSACTION;

WITH order_data AS (
    SELECT order_id, total
    FROM (
        VALUES (1, 100.0),
               (2, 200.0)
    ) AS order_data (order_id, total)
),
updated_data AS (
    SELECT order_id, 150.0 AS total
    FROM (
        VALUES (1, 100.0),
               (2, 200.0)
    ) AS order_data (order_id, total)
)

SELECT od.order_id, ud.total AS new_total
FROM order_data od
INNER JOIN updated_data ud ON od.order_id = ud.order_id;

COMMIT;