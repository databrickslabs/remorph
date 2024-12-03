--Query type: DCL
DECLARE @customer_id INT;
SELECT *
FROM (
    VALUES (1, 'Customer#000000001'),
           (2, 'Customer#000000002')
) AS customers (customer_id, customer_name)
WHERE customer_id = @customer_id;
