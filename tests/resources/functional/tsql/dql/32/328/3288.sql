-- tsql sql:
WITH temp_result AS ( SELECT 'This is a sample description' AS description UNION ALL SELECT 'This is another sample description' AS description ) SELECT description FROM temp_result WHERE description LIKE '%performance%';
