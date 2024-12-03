--Query type: DDL
CREATE SEQUENCE seq_01
    START WITH 1
    INCREMENT BY 1;

CREATE TABLE sequence_test_table
(
    i INTEGER
);

WITH temp_result AS
(
    SELECT 1 AS i
    UNION ALL
    SELECT i + 1
    FROM temp_result
    WHERE i < 10
)
INSERT INTO sequence_test_table
SELECT *
FROM temp_result
OPTION (MAXRECURSION 0);

SELECT *
FROM sequence_test_table;

-- REMORPH CLEANUP: DROP TABLE sequence_test_table;
-- REMORPH CLEANUP: DROP SEQUENCE seq_01;
