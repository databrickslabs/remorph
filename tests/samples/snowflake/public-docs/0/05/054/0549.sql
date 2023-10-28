SELECT
    column1,
    CASE 
        WHEN column1 = 1 THEN 'one'
        WHEN column1 = 2 THEN 'two'
        WHEN column1 IS NULL THEN 'NULL'
        ELSE 'other'
    END AS result
FROM VALUES (1), (2), (NULL);