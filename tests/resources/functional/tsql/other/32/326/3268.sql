--Query type: DDL
CREATE TABLE customer_info (
    customer_id VARBINARY(85) DEFAULT SUSER_SID(),
    customer_name VARCHAR(30) DEFAULT SYSTEM_USER,
    customer_dept VARCHAR(10) DEFAULT 'MARKETING',
    order_date DATETIME DEFAULT GETDATE()
);
INSERT INTO customer_info (
    customer_id,
    customer_name,
    customer_dept,
    order_date
)
VALUES (
    DEFAULT,
    DEFAULT,
    DEFAULT,
    DEFAULT
);