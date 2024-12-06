-- tsql sql:
CREATE TABLE customer_demo
(
    c1 INT IDENTITY(1,1) PRIMARY KEY,
    c_custkey INT,
    c_name VARCHAR(25),
    c_address VARCHAR(40),
    c_nationkey INT,
    c_phone VARCHAR(15),
    c_acctbal DECIMAL(15, 2),
    c_mktsegment VARCHAR(10),
    c_comment VARCHAR(117)
);

INSERT INTO customer_demo (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
VALUES
(1, 'Customer#000000001', '1310.0', 15, '25-989-741-2988', 2106.86, 'BUILDING', 'regular future accounts. blithely ironic instructions according to final dependencies. slyly bold');

INSERT INTO customer_demo (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
FROM (
VALUES
(2, 'Customer#000000002', '4170.0', 14, '14-128-190-5944', 4773.00, 'AUTOMOBILE', 'pending deposits. quickly ironic instruction'),
(3, 'Customer#000000003', '673.0', 3, '25-989-741-2988', 2106.86, 'BUILDING', 'regular future accounts. blithely ironic instructions according to final dependencies. slyly bold')
) AS subquery (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment);

INSERT INTO customer_demo (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
FROM (
VALUES
(4, 'Customer#000000004', '4170.0', 14, '14-128-190-5944', 4773.00, 'AUTOMOBILE', 'pending deposits. quickly ironic instruction'),
(5, 'Customer#000000005', '673.0', 3, '25-989-741-2988', 2106.86, 'BUILDING', 'regular future accounts. blithely ironic instructions according to final dependencies. slyly bold')
) AS subquery (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment);

SELECT * FROM customer_demo;

-- REMORPH CLEANUP: DROP TABLE customer_demo;
