--Query type: DQL
SELECT T1.PurchaseOrderID, T1.EmployeeID, T2.VendorID
FROM (
    VALUES (1, 10, 100),
           (2, 20, 200),
           (3, 30, 300)
) AS T1 (
    PurchaseOrderID,
    EmployeeID,
    VendorID
)
INNER JOIN (
    VALUES (100, 'Vendor1'),
           (200, 'Vendor2'),
           (300, 'Vendor3')
) AS T2 (
    VendorID,
    VendorName
)
ON T1.VendorID = T2.VendorID
