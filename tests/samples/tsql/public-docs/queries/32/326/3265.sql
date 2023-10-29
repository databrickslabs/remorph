-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/session-user-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
CREATE TABLE deliveries3  
(  
 order_id INT IDENTITY(5000, 1) NOT NULL,  
 cust_id  INT NOT NULL,  
 order_date SMALLDATETIME NOT NULL DEFAULT GETDATE(),  
 delivery_date SMALLDATETIME NOT NULL DEFAULT   
    DATEADD(dd, 10, GETDATE()),  
 received_shipment NCHAR(30) NOT NULL DEFAULT SESSION_USER  
);  
GO