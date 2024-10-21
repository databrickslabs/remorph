--Query type: DML
INSERT orders_new (cust_id, order_amt)
SELECT *
FROM (
    VALUES (5106, 578.95),
           (5107, 579.95),
           (5108, 580.95)
) AS temp_result (cust_id, order_amt);