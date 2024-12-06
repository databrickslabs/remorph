-- tsql sql:
CREATE TABLE #DimCustomer_upsert
(
    [CustomerKey] INT,
    [CompanyName] VARCHAR(255),
    [AddressLine1] VARCHAR(255)
);

INSERT INTO #DimCustomer_upsert
SELECT      [CustomerKey],
           [CompanyName],
           [AddressLine1]
FROM      (
            VALUES
            (1, 'Customer 1', 'Address 1'),
            (2, 'Customer 2', 'Address 2'),
            (3, 'Customer 3', 'Address 3')
          ) AS c ([CustomerKey], [CompanyName], [AddressLine1]);

MERGE #DimCustomer_upsert AS target
USING (
    SELECT      [CustomerKey],
    ,           [CompanyName],
    ,           [AddressLine1]
    FROM      (
                VALUES
                (4, 'Customer 4', 'Address 4'),
                (5, 'Customer 5', 'Address 5'),
                (6, 'Customer 6', 'Address 6')
              ) AS c ([CustomerKey], [CompanyName], [AddressLine1])
) AS source
ON target.[CustomerKey] = source.[CustomerKey]
WHEN NOT MATCHED THEN
    INSERT ([CustomerKey], [CompanyName], [AddressLine1])
    VALUES (source.[CustomerKey], source.[CompanyName], source.[AddressLine1]);

SELECT * FROM #DimCustomer_upsert;

-- REMORPH CLEANUP: DROP TABLE #DimCustomer_upsert;
