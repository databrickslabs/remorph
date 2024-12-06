-- tsql sql:
IF OBJECT_ID('dbo.NewCustomers', 'U') IS NOT NULL
    DROP TABLE dbo.NewCustomers;

CREATE TABLE dbo.NewCustomers
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

WITH NewCustomersCTE AS
(
    SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
    FROM (
        VALUES
            (1, 'Customer#000000001', '1310.0', 15, '25-989-741-2988', 711.56, 'BUILDING', 'regular future accounts'),
            (2, 'Customer#000000002', '1520.0', 15, '25-989-741-2989', 711.56, 'BUILDING', 'regular future accounts')
    ) AS NewCustomers (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
)
SELECT *
INTO #NewCustomers
FROM NewCustomersCTE;

-- REMORPH CLEANUP: DROP TABLE #NewCustomers;
