-- tsql sql:
DECLARE @order_date DATE = GETDATE();

SELECT FORMAT(o.order_date, 'dd/MM/yyyy', 'en-US') AS [Order Date]
       , FORMAT(o.total_price, '###-##-####') AS [Total Price]
FROM (
    VALUES (
        (@order_date, 123456789.99)
    )
) AS o (order_date, total_price);
