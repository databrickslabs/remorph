-- tsql sql:
CREATE TABLE SalesData
(
    s_suppkey INT,
    s_name VARCHAR(255),
    s_address VARCHAR(255),
    s_phone VARCHAR(20),
    s_acctbal DECIMAL(10, 2),
    s_comment VARCHAR(255)
);

CREATE INDEX idx_SalesData
ON SalesData (s_suppkey);

INSERT INTO SalesData (s_suppkey, s_name, s_address, s_phone, s_acctbal, s_comment)
SELECT s_suppkey, s_name, s_address, s_phone, s_acctbal, s_comment
FROM (
    VALUES
    (
        1,
        'Supplier#000000001',
        '123 Main St',
        '123-456-7890',
        100.00,
        'Comment'
    ),
    (
        2,
        'Supplier#000000002',
        '456 Elm St',
        '987-654-3210',
        200.00,
        'Comment'
    ),
    (
        3,
        'Supplier#000000003',
        '789 Oak St',
        '555-123-4567',
        300.00,
        'Comment'
    )
) AS SalesData (s_suppkey, s_name, s_address, s_phone, s_acctbal, s_comment);

ALTER INDEX idx_SalesData
ON SalesData
REORGANIZE PARTITION = ALL
WITH (COMPRESS_ALL_ROW_GROUPS = ON);

SELECT *
FROM SalesData;
