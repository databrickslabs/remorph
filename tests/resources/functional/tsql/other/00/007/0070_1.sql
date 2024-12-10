-- tsql sql:
CREATE TABLE customer_info (id INT, email VARCHAR(255), dob DATE);
ALTER TABLE customer_info ALTER COLUMN email ADD MASKED WITH (FUNCTION = 'email()');
ALTER TABLE customer_info ALTER COLUMN dob ADD MASKED WITH (FUNCTION = 'default()');
ALTER TABLE customer_info ALTER COLUMN email DROP MASKED;
ALTER TABLE customer_info ALTER COLUMN dob DROP MASKED;
WITH customer_info_cte AS (
    SELECT id, email, dob
    FROM customer_info
)
SELECT *
FROM customer_info_cte;
