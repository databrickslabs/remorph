-- tsql sql:
CREATE PARTITION FUNCTION pf_order_date (DATE) AS RANGE RIGHT FOR VALUES ('2004-01-01', '2005-01-01', '2006-01-01', '2007-01-01');
CREATE PARTITION SCHEME ps_order_date AS PARTITION pf_order_date ALL TO ('PRIMARY');
CREATE TABLE Customer_Orders (
    customer_id INT,
    customer_city VARCHAR(25),
    order_date DATE,
    last_update_date DATE
) ON ps_order_date (order_date);
