-- tsql sql:
INSERT INTO customers (customer_ID, last_name, region_ID)
SELECT customer_ID, last_name, region_ID
FROM (
    VALUES (201, 'Smith', 1),
           (202, 'Jones', 1),
           (203, 'Williams', 2)
) AS temp_result_set (customer_ID, last_name, region_ID);
