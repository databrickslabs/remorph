-- tsql sql:
INSERT INTO customer_data (customer_id, customer_name)
SELECT *
FROM (
    VALUES (1, 'John Doe'),
           (2, 'Jane Doe'),
           (3, 'Bob Smith')
) AS temp_result_set (customer_id, customer_name);
