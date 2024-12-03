--Query type: DDL
CREATE TABLE customer_temp (c_custkey INT, c_comment VARCHAR(MAX));
INSERT INTO customer_temp (c_custkey, c_comment)
VALUES (1, 'comment');
CREATE FULLTEXT INDEX ON customer_temp (c_comment)
KEY INDEX c_custkey
WITH SEARCH PROPERTY LIST = spl_customer;
SELECT *
FROM customer_temp;
-- REMORPH CLEANUP: DROP TABLE customer_temp;
-- REMORPH CLEANUP: DROP FULLTEXT INDEX ON customer_temp;
