--Query type: DDL
CREATE TABLE [dbo].[SupplierDetails]
(
    [SupplierID] INT,
    [SupplierName] VARCHAR(50),
    [Address] VARCHAR(100)
);

INSERT INTO [dbo].[SupplierDetails]
(
    [SupplierID],
    [SupplierName],
    [Address]
)
VALUES
(
    1,
    'Supplier1',
    'Address1'
),
(
    2,
    'Supplier2',
    'Address2'
);

SELECT *
FROM [dbo].[SupplierDetails];

-- REMORPH CLEANUP: DROP TABLE [dbo].[SupplierDetails];
