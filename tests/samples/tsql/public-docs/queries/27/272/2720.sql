-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-using-pivot-and-unpivot?view=sql-server-ver16

SELECT PurchaseOrderID, EmployeeID, VendorID  
FROM PurchaseOrderHeader;