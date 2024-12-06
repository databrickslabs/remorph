-- tsql sql:
CREATE PROCEDURE get_customer_config
AS
BEGIN
    SELECT *
    FROM (
        VALUES (1, 'John', 'Doe'),
               (2, 'Jane', 'Doe')
    ) AS customer_data(customer_id, first_name, last_name);
END;
EXEC get_customer_config;
