--Query type: DDL
CREATE TABLE temp_values (i INT);
WITH temp_result AS (
    SELECT i
    FROM (
        VALUES (1)
    ) AS temp (i)
)
INSERT INTO temp_values (i)
SELECT i
FROM temp_result;