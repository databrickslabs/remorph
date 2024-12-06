-- tsql sql:
CREATE TABLE orders
(
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus CHAR(1),
    o_totalprice DECIMAL(10, 2),
    o_orderdate DATE,
    o_orderpriority VARCHAR(10),
    o_clerk VARCHAR(20),
    o_shippriority INT,
    o_comment VARCHAR(100)
);

INSERT INTO orders
VALUES
    (1, 10, 'O', 10.00, '1992-01-01', '5-LOW', 'Clerk#000000001', 0, 'g. foxes wake quickly. blithe dogs sleep soundly.'),
    (2, 20, 'O', 20.00, '1992-01-02', '1-URGENT', 'Clerk#000000002', 1, 'blithe dogs wake quickly. foxes sleep soundly.');

WITH order_data AS
(
    SELECT 1 AS o_orderkey, 10 AS o_custkey, 'O' AS o_orderstatus, 10.00 AS o_totalprice, '1992-01-01' AS o_orderdate, '5-LOW' AS o_orderpriority, 'Clerk#000000001' AS o_clerk, 0 AS o_shippriority, 'g. foxes wake quickly. blithe dogs sleep soundly.' AS o_comment
    UNION ALL
    SELECT 2, 20, 'O', 20.00, '1992-01-02', '1-URGENT', 'Clerk#000000002', 1, 'blithe dogs wake quickly. foxes sleep soundly.'
)
SELECT *
FROM order_data;
