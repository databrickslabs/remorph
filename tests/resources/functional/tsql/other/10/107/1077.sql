--Query type: DDL
CREATE PROC Get_Supplier_Name
    @SupplierID INT
AS
BEGIN
    SELECT S_NAME
    FROM (
        VALUES (1, 'Supplier#000000001'),
               (2, 'Supplier#000000002')
    ) AS Supplier(SupplierID, S_NAME)
    WHERE SupplierID = @SupplierID;
END;