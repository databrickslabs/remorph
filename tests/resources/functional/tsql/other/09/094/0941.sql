--Query type: DDL
CREATE DATABASE [new-database]
COLLATE SQL_Latin1_General_CP1_CS_AS
WITH CATALOG_COLLATION = DATABASE_DEFAULT;

SELECT *
FROM (
    VALUES ('1-URGENT', 100.0, '1993-07-01', 1),
           ('2-HIGH', 200.0, '1993-08-01', 2),
           ('3-MEDIUM', 300.0, '1993-09-01', 3)
) AS temp_result (order_priority, revenue, order_date, ship_priority);
