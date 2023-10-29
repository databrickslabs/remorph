-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/session-user-transact-sql?view=sql-server-ver16

SELECT order_id AS 'Order #', cust_id AS 'Customer #',   
   delivery_date AS 'When Delivered', received_shipment   
   AS 'Received By'  
FROM deliveries3  
ORDER BY order_id;  
GO