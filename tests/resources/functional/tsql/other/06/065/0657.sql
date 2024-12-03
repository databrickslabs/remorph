--Query type: DML
CREATE TABLE array_example (array_column sql_variant);

WITH temp_result AS (
    SELECT value
    FROM (
        VALUES (12), ('twelve'), (NULL)
    ) AS T(value)
)
INSERT INTO array_example (array_column)
SELECT value
FROM temp_result;

SELECT *
FROM array_example;

-- REMORPH CLEANUP: DROP TABLE array_example;
