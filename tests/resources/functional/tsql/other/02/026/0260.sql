--Query type: DDL
CREATE TABLE #ext_order_details
(
    order_date date,
    order_total decimal(10, 2),
    order_id integer
);

INSERT INTO #ext_order_details
(
    order_date,
    order_total,
    order_id
)
VALUES
(
    '2022-01-01',
    100.00,
    1
),
(
    '2022-01-02',
    200.00,
    2
),
(
    '2022-01-03',
    300.00,
    3
);

SELECT *
FROM #ext_order_details;

-- REMORPH CLEANUP: DROP TABLE #ext_order_details;
