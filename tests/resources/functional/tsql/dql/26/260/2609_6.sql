--Query type: DQL
WITH customer_data AS ( SELECT 'Hello %20s!' AS format_string, 'TEST' AS customer_name ) SELECT FORMATMESSAGE(format_string, customer_name) AS formatted_message FROM customer_data;
