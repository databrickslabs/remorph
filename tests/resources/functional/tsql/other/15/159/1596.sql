--Query type: DML
DECLARE @Order XML;
SET @Order = '<order><customerID>123</customerID><orderDate>2022-01-01</orderDate><total>100.00</total></order>';

WITH OrderCTE AS (
    SELECT @Order AS OrderXML
)
SELECT 
    OrderXML.value('(/order/customerID)[1]', 'int') AS CustomerID,
    OrderXML.value('(/order/orderDate)[1]', 'date') AS OrderDate,
    OrderXML.value('(/order/total)[1]', 'decimal(10, 2)') AS Total
FROM OrderCTE;