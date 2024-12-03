--Query type: DML
CREATE TABLE combined
(
    order_key INTEGER,
    cust_key INTEGER,
    order_status VARCHAR,
    total_price DECIMAL(10, 2),
    order_date DATE,
    part_key INTEGER,
    supp_key INTEGER,
    extended_price DECIMAL(10, 2),
    discount DECIMAL(10, 2)
);

INSERT INTO combined
(
    order_key,
    cust_key,
    order_status,
    total_price,
    order_date,
    part_key,
    supp_key,
    extended_price,
    discount
)
VALUES
(
    1,
    1,
    'O',
    100.00,
    '1992-01-01',
    1,
    1,
    100.00,
    0.1
),
(
    1,
    1,
    'O',
    100.00,
    '1992-01-01',
    2,
    2,
    200.00,
    0.2
),
(
    2,
    2,
    'O',
    200.00,
    '1992-01-02',
    3,
    3,
    300.00,
    0.3
);
