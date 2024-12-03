--Query type: DML
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerData')
BEGIN
    CREATE TABLE CustomerData
    (
        c_custkey INT,
        c_name VARCHAR(255),
        c_address VARCHAR(255),
        c_nationkey INT,
        c_phone VARCHAR(255),
        c_acctbal DECIMAL(10, 2),
        c_mktsegment VARCHAR(255),
        c_comment VARCHAR(255)
    );
END;

WITH CustomerDataCTE AS
(
    SELECT *
    FROM
    (
        SELECT *
        FROM OPENROWSET
        (
            BULK 'C:\data\customer_data.csv',
            FORMATFILE = 'C:\data\format_no_collation.txt',
            CODEPAGE = '65001'
        ) AS bulk_rowset
    ) AS subquery
)
INSERT INTO CustomerData
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
SELECT *
FROM CustomerDataCTE;

SELECT *
FROM CustomerData;
-- REMORPH CLEANUP: DROP TABLE CustomerData;
