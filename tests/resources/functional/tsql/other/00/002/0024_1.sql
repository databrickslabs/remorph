--Query type: DDL
CREATE TABLE customer_region (r_name nvarchar(50) COLLATE French_CI_AS);
INSERT INTO customer_region (r_name)
VALUES ('Europe'), ('Asia'), ('North America');
SELECT * FROM customer_region;
-- REMORPH CLEANUP: DROP TABLE customer_region;
