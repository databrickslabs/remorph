--Query type: DQL
WITH temp_result AS ( SELECT 'Customer' AS name, 'Comment' AS comment FROM ( VALUES (1) ) AS t (c) ) SELECT CONCAT(name, comment) AS result FROM temp_result
