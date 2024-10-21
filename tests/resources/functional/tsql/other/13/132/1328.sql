--Query type: DDL
CREATE TABLE customer_orders
(
    c_custkey INT,
    c_name VARCHAR(25),
    c_address VARCHAR(40),
    c_nationkey INT,
    c_phone VARCHAR(15),
    c_acctbal DECIMAL(15, 2),
    c_mktsegment VARCHAR(10),
    c_comment VARCHAR(117)
);

INSERT INTO customer_orders
(
    c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    c_acctbal,
    c_mktsegment,
    c_comment
)
VALUES
(
    1,
    'John',
    '123 Main St',
    1,
    '123-456-7890',
    100.00,
    'Retail',
    'Comment'
);

SELECT *
FROM customer_orders;

-- REMORPH CLEANUP: DROP TABLE customer_orders;