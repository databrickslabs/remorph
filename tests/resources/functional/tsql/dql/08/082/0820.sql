--Query type: DQL
WITH temp_result AS ( SELECT * FROM customer ) SELECT TOP 10 * FROM temp_result ORDER BY NEWID();
