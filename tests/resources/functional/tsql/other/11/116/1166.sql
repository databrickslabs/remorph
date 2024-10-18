--Query type: DDL
CREATE TABLE #Customer
(
    c_custkey INT,
    c_email VARCHAR(50)
);

INSERT INTO #Customer (c_custkey, c_email)
VALUES
    (1, 'customer1@example.com'),
    (2, 'customer2@example.com'),
    (3, 'customer3@example.com');

CREATE STATISTICS CustomerMail1
ON #Customer (c_custkey, c_email)
WITH SAMPLE 10 PERCENT;

SELECT *
FROM #Customer;

-- REMORPH CLEANUP: DROP TABLE #Customer;
-- REMORPH CLEANUP: DROP STATISTICS #Customer.CustomerMail1;