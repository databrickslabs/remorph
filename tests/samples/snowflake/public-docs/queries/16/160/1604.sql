-- see https://docs.snowflake.com/en/sql-reference/functions/any_value

SELECT customer.id , ANY_VALUE(customer.name) , SUM(orders.value)
    FROM customer
    JOIN orders ON customer.id = orders.customer_id
    GROUP BY customer.id;