--Query type: DCL
CREATE TABLE customer_names (customer_name sysname);
INSERT INTO customer_names (customer_name)
VALUES ('customer');
CREATE LOGIN customer_login
WITH PASSWORD = 'password';
CREATE USER customer_user
FOR LOGIN customer_login;
WITH customer_cte AS (
    SELECT customer_name
    FROM (
        VALUES ('customer')
    ) AS customer_names (customer_name)
)
SELECT *
FROM customer_cte;
SELECT *
FROM (
    VALUES ('customer')
) AS customer_names (customer_name);
SELECT *
FROM customer_names;
-- REMORPH CLEANUP: DROP TABLE customer_names;
-- REMORPH CLEANUP: DROP USER customer_user;
-- REMORPH CLEANUP: DROP LOGIN customer_login;
