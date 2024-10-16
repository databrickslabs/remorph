--Query type: DQL
SELECT FORMATMESSAGE(format_string, customer_name) AS formatted_message FROM (VALUES ('Hello %-20s!', 'TEST')) AS customer_info(format_string, customer_name);