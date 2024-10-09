--Query type: DML
CREATE TABLE orders (
    order_key INTEGER,
    cust_key INTEGER,
    order_status VARCHAR,
    total_price DECIMAL,
    order_date DATE,
    order_priority VARCHAR,
    clerk VARCHAR,
    ship_priority INTEGER,
    comment VARCHAR
);

INSERT INTO orders (
    order_key,
    cust_key,
    order_status,
    total_price,
    order_date,
    order_priority,
    clerk,
    ship_priority,
    comment
)
VALUES
    (1, 1, 'O', 100.00, '1992-01-01', '1-URGENT', 'Clerk#000000001', 0, 'O'),
    (2, 2, 'O', 200.00, '1992-01-02', '2-HIGH', 'Clerk#000000002', 0, 'O'),
    (3, 3, 'O', 300.00, '1992-01-03', '3-MEDIUM', 'Clerk#000000003', 0, 'O'),
    (4, 4, 'O', 400.00, '1992-01-04', '4-NOT SPECIFIED', 'Clerk#000000004', 0, 'O'),
    (5, 5, 'O', 500.00, '1992-01-05', '5-LOW', 'Clerk#000000005', 0, 'O');