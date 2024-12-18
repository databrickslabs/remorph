-- tsql sql:
CREATE TABLE demo_volatile (i INTEGER);
INSERT INTO demo_volatile
SELECT *
FROM (
    VALUES (1)
) AS temp_result (i);
