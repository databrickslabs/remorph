--Query type: DDL
CREATE PROCEDURE find_customers @customer_name sysname = NULL
AS
BEGIN
    IF @customer_name IS NULL
    BEGIN
        PRINT 'You must give a customer name';
        RETURN;
    END
    ELSE
    BEGIN
        WITH customers AS (
            SELECT 'John' AS name, 1 AS id, 101 AS cid
            UNION ALL
            SELECT 'Jane' AS name, 2 AS id, 102 AS cid
            UNION ALL
            SELECT 'Bob' AS name, 3 AS id, 103 AS cid
        ),
        orders AS (
            SELECT 1 AS id, 101 AS cid, 'Order 1' AS order_name
            UNION ALL
            SELECT 2 AS id, 102 AS cid, 'Order 2' AS order_name
            UNION ALL
            SELECT 3 AS id, 103 AS cid, 'Order 3' AS order_name
        )
        SELECT c.name, c.id, o.order_name
        FROM customers c
        INNER JOIN orders o ON c.cid = o.cid
        WHERE c.name = @customer_name;
    END
END;
EXEC find_customers 'John';