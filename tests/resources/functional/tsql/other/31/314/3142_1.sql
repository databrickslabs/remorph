--Query type: DDL
IF OBJECT_ID('dbo.CustomerOne', 'U') IS NOT NULL
    DROP TABLE dbo.CustomerOne;

CREATE TABLE dbo.CustomerOne
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

WITH CustomerCTE AS
(
    SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
    FROM (
        VALUES
            (1, 'Customer#001', '123 Main St', 1, '123-456-7890', 100.00, 'BUILDING', 'This is a comment'),
            (2, 'Customer#002', '456 Elm St', 2, '987-654-3210', 200.00, 'AUTOMOBILE', 'This is another comment')
    ) AS CustomerTable (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
)
SELECT *
FROM CustomerCTE;
-- REMORPH CLEANUP: DROP TABLE dbo.CustomerOne;
