--Query type: DQL
WITH customer_info AS ( SELECT 'Please ensure the door is locked!' AS customer_comment ) SELECT position = PATINDEX('%en_ure%', customer_comment) FROM customer_info