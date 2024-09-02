--Query type: DDL
CREATE TABLE minhash_b_3 (mh VARBINARY(MAX));
INSERT INTO minhash_b_3 (mh)
SELECT CAST(CHECKSUM(i) AS VARBINARY(MAX))
FROM (
    SELECT i
    FROM (
        VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11)
    ) AS temp(i)
) AS temp_result
WHERE i > 5;
SELECT * FROM minhash_b_3;
-- REMORPH CLEANUP: DROP TABLE minhash_b_3;