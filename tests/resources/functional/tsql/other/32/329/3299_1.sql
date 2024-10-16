--Query type: DDL
SET NOCOUNT ON;
CREATE TABLE orders24
(
    order_id INT IDENTITY(1000, 1) NOT NULL,
    cust_id INT NOT NULL,
    order_date SMALLDATETIME NOT NULL DEFAULT GETDATE(),
    order_amt MONEY NOT NULL,
    order_person CHAR(30) NOT NULL DEFAULT CURRENT_USER
);

WITH ordersCTE AS
(
    SELECT 1000 AS order_id, 1 AS cust_id, GETDATE() AS order_date, 100.00 AS order_amt, CURRENT_USER AS order_person
    UNION ALL
    SELECT 1001, 2, GETDATE(), 200.00, CURRENT_USER
)
SELECT order_id, cust_id, order_date, order_amt, order_person
FROM ordersCTE;