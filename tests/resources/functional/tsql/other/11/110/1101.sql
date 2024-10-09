--Query type: DDL
CREATE PROCEDURE pr_SupplierNames
    @VarDiscount decimal(5, 2)
AS
BEGIN
    PRINT 'Suppliers with discount greater than ' + CAST(@VarDiscount AS varchar(10));

    WITH SupplierCTE AS (
        SELECT S_SUPPKEY, S_NAME, S_DISCOUNT
        FROM Suppliers
    )
    SELECT S_NAME, S_DISCOUNT
    FROM SupplierCTE
    WHERE S_DISCOUNT > @VarDiscount;

END

EXEC pr_SupplierNames 0.10;

SELECT * FROM Suppliers;