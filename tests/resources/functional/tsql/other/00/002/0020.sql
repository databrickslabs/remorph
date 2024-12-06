-- tsql sql:
DROP TABLE IF EXISTS soybean_production;
CREATE TABLE soybean_production
(
    producer_ID INTEGER,
    region VARCHAR,
    quantity FLOAT
);
INSERT INTO soybean_production (producer_ID, region, quantity)
VALUES
    (1, 'Illinois', 200),
    (2, 'Indiana', 210),
    (3, 'Ohio', 220),
    (4, 'Michigan', 230);
SELECT *
FROM soybean_production;
-- REMORPH CLEANUP: DROP TABLE soybean_production;
