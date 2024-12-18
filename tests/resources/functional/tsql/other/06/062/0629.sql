-- tsql sql:
WITH temp_result AS (
    SELECT 'Test' AS column1, 'Data' AS column2
)
SELECT CASE WHEN column1 = 'Test' THEN 'I caught the expected exception.' ELSE 'If you see this, I did not catch any exception.' END AS result
FROM temp_result;
-- REMORPH CLEANUP: DROP TABLE temp_result;
