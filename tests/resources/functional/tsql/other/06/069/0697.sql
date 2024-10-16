--Query type: DML
CREATE TABLE sf_customers
(
    c_custkey INT,
    c_name VARCHAR(25),
    c_address VARCHAR(40),
    c_city VARCHAR(10),
    c_nation VARCHAR(15),
    c_region VARCHAR(12),
    c_phone VARCHAR(15),
    c_mktsegment VARCHAR(10)
);

WITH customers AS
(
    SELECT c_custkey, c_name, c_address, c_city, c_nation, c_region, c_phone, c_mktsegment
    FROM (
        VALUES
            (1, 'Customer#000000001', '1310.0', 'UNITED KI1', 'UNITED KI1', 'EUROPE', '23-743-935-0687', 'BUILDING'),
            (2, 'Customer#000000002', '1520.0', 'UNITED KI1', 'UNITED KI1', 'EUROPE', '17-982-835-2687', 'AUTOMOBILE'),
            (3, 'Customer#000000003', '1830.0', 'UNITED KI1', 'UNITED KI1', 'EUROPE', '11-723-935-0687', 'MACHINERY')
    ) AS customer (c_custkey, c_name, c_address, c_city, c_nation, c_region, c_phone, c_mktsegment)
)
INSERT INTO sf_customers
SELECT *
FROM customers
WHERE c_city = 'UNITED KI1';

SELECT *
FROM sf_customers;
-- REMORPH CLEANUP: DROP TABLE sf_customers;