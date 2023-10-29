-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-synonym-transact-sql?view=sql-server-ver16

-- Creating the dbo.OrderDozen function
CREATE FUNCTION dbo.OrderDozen (@OrderAmt INT)
RETURNS INT
    WITH EXECUTE AS CALLER
AS
BEGIN
    IF @OrderAmt % 12 <> 0
    BEGIN
        SET @OrderAmt += 12 - (@OrderAmt % 12)
    END

    RETURN (@OrderAmt);
END;
GO

-- Using the dbo.OrderDozen function
DECLARE @Amt INT;

SET @Amt = 15;

SELECT @Amt AS OriginalOrder,
    dbo.OrderDozen(@Amt) AS ModifiedOrder;

-- Create a synonym dbo.CorrectOrder for the dbo.OrderDozen function.
CREATE SYNONYM dbo.CorrectOrder
FOR dbo.OrderDozen;
GO

-- Using the dbo.CorrectOrder synonym.
DECLARE @Amt INT;

SET @Amt = 15;

SELECT
    @Amt AS OriginalOrder,
    dbo.CorrectOrder(@Amt) AS ModifiedOrder;