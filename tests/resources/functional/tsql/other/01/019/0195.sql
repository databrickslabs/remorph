-- tsql sql:
BEGIN TRANSACTION;

WITH order_data AS (
	SELECT *
	FROM (
		VALUES (1, 100.0), (2, 200.0)
	) AS data (order_id, total)
)

INSERT INTO orders (order_id, total)

SELECT order_id, total
FROM order_data;

COMMIT;
