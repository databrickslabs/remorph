--Query type: DCL
CREATE TABLE temp_result (customer_name VARCHAR(50));
INSERT INTO temp_result (customer_name)
VALUES ('customer');
GRANT UPDATE ON temp_result TO [Sally];
SELECT * FROM temp_result;
-- REMORPH CLEANUP: DROP TABLE temp_result;
