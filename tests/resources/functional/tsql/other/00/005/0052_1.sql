-- tsql sql:
CREATE TABLE #customer_clone
(
    customer_key INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

INSERT INTO #customer_clone
(
    customer_key,
    first_name,
    last_name
)
SELECT customer_key, first_name, last_name
FROM customer;

MERGE INTO #customer_clone AS target
USING (
    VALUES (1, 'John', 'Doe'),
           (2, 'Jane', 'Doe')
) AS src (customer_key, first_name, last_name)
ON target.customer_key = src.customer_key
WHEN MATCHED AND src.customer_key <= 2 THEN DELETE;

SELECT *
FROM #customer_clone;
-- REMORPH CLEANUP: DROP TABLE #customer_clone;
