--Query type: DML
CREATE TABLE #Customer
(
    C_CustomerKey INT,
    C_Name VARCHAR(255),
    C_Address VARCHAR(255),
    C_NationKey INT,
    C_Phone VARCHAR(25),
    C_AcctBal DECIMAL(18, 2),
    C_MktSegment VARCHAR(10),
    C_Comment VARCHAR(117)
);

INSERT INTO #Customer
(
    C_CustomerKey,
    C_Name,
    C_Address,
    C_NationKey,
    C_Phone,
    C_AcctBal,
    C_MktSegment,
    C_Comment
)
VALUES
(
    1,
    'Customer 1',
    'Address 1',
    1,
    '123-456-7890',
    1000.00,
    'BUILDING',
    'Comment 1'
),
(
    2,
    'Customer 2',
    'Address 2',
    2,
    '987-654-3210',
    2000.00,
    'AUTOMOBILE',
    'Comment 2'
);

SELECT *
FROM #Customer;
-- REMORPH CLEANUP: DROP TABLE #Customer;
