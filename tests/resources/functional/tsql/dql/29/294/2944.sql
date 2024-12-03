--Query type: DQL
WITH temp_result AS ( SELECT customer_id FROM customer ) SELECT customer_id FROM temp_result;
