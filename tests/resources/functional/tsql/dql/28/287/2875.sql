--Query type: DQL
WITH temp_result AS ( SELECT 'search_column' AS column_name FROM ( VALUES ('search_column') ) AS search_table ( column_name ) ) SELECT column_name FROM temp_result WHERE column_name LIKE '%new_search_property%';
