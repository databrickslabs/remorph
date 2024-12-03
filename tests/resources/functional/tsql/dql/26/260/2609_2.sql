--Query type: DQL
SELECT FORMATMESSAGE('Unsigned decimal %d, %d', num1, num2) FROM (VALUES (50, -50)) AS numbers(num1, num2);
