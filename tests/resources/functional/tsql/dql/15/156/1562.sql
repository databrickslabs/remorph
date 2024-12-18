-- tsql sql:
DECLARE @order_date DATETIME2 = '2020-06-15 21:22:11';
DECLARE @reference_date DATETIME2 = '2019-01-01 00:00:00';

WITH order_data AS (
    SELECT @order_date AS order_date, @reference_date AS reference_date
)

SELECT DATE_BUCKET(WEEK, 5, order_date, reference_date) AS order_week
FROM order_data;
