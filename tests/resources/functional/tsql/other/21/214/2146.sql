--Query type: DML
WITH temp_result AS (
    SELECT 1 AS level
)
SELECT 
    CASE 
        WHEN level > 5 THEN 'This statement nested over 5 levels of triggers.'
        ELSE ''
    END AS message
FROM temp_result;