-- tsql sql:
SELECT TOP 1
    YEAR(0) AS year_value,
    MONTH(0) AS month_value,
    DAY(0) AS day_value
FROM (
    VALUES (1)
) AS customer_table (customer_id);
