-- tsql sql:
WITH CustomerCTE AS (SELECT 'Hello %s!' AS format_string, 'TEST' AS param_value)
SELECT FORMATMESSAGE(format_string, param_value) AS formatted_string
FROM CustomerCTE;
