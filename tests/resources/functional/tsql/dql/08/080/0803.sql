-- tsql sql:
WITH customer_info AS (SELECT 'This ' + 'is ' + 'another ' + 'concatenation ' + 'technique.' AS customer_name) SELECT customer_name FROM customer_info
