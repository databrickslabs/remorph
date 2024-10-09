--Query type: DQL
SELECT CEILING(amount) AS rounded_amount FROM (VALUES (123.45), (-123.45), (0.0)) AS order_total(amount);