--Query type: TCL
BEGIN TRANSACTION;
WITH temp_result AS (
    SELECT 1 AS o_orderkey, 100 AS o_totalprice
)
INSERT INTO orders (o_orderkey, o_totalprice)
SELECT o_orderkey, o_totalprice * 1.1 AS new_totalprice
FROM temp_result;
COMMIT;