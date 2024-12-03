--Query type: DDL
SELECT *
INTO #customer_table
FROM (
    VALUES (
        1, 'John Doe', '123 Main St'
    )
) AS customer_table (
    customer_key,
    customer_name,
    customer_address
);

ALTER TABLE #customer_table
ADD customer_email VARCHAR(50) NULL;

ALTER TABLE #customer_table
ADD CONSTRAINT customer_email_unique UNIQUE (customer_email);

SELECT *
FROM #customer_table;

-- REMORPH CLEANUP: DROP TABLE #customer_table;
