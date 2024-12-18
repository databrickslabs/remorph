-- tsql sql:
SELECT FORMATMESSAGE('Unsigned decimal with prefix: %u, %u', num1, num2) FROM (VALUES (50, -50)) AS numbers(num1, num2);
