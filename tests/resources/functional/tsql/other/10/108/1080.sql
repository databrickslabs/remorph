--Query type: DDL
CREATE PROCEDURE Sales.Update_LineItemOrderKey
    @NewOrderKey INTEGER,
    @Rowcount INT OUTPUT
AS
SET NOCOUNT ON;

WITH LineItemCTE AS (
    SELECT l_orderkey, l_extendedprice, l_discount
    FROM (
        VALUES (1, 100.00, 0.1), (2, 200.00, 0.2), (3, 300.00, 0.3)
    ) AS LineItem (l_orderkey, l_extendedprice, l_discount)
)
UPDATE LineItemCTE
SET l_orderkey = (
    CASE
        WHEN l_discount > 0.1 THEN @NewOrderKey
        ELSE l_orderkey
    END
)
WHERE l_extendedprice > 200.00;

SET @Rowcount = @@rowcount;