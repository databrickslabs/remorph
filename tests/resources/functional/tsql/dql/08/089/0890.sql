--Query type: DQL
WITH temp_result AS ( SELECT 1 AS id, 'John' AS first_name, 'Doe' AS last_name UNION ALL SELECT 2, 'Jane', 'Doe' ) SELECT * FROM temp_result;
