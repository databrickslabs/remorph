--Query type: DDL
CREATE TABLE r1 (r_regionkey INT, r_name VARCHAR(255));
WITH cte AS (
    SELECT * FROM (VALUES (1, 'ASIA'), (2, 'EUROPE'), (3, 'AFRICA')) AS r1(r_regionkey, r_name)
    WHERE r_regionkey > 1 AND r_name IN ('ASIA', 'EUROPE', 'AMERICA')
)
INSERT INTO r1 (r_regionkey, r_name)
SELECT * FROM cte;
SELECT * FROM r1;
-- REMORPH CLEANUP: DROP TABLE r1;
