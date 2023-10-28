CREATE TRANSIENT TABLE store_sales (
    branch_ID    INTEGER,
    city        VARCHAR,
    gross_sales NUMERIC(9, 2),
    gross_costs NUMERIC(9, 2),
    net_profit  NUMERIC(9, 2)
    );

INSERT INTO store_sales (branch_ID, city, gross_sales, gross_costs)
    VALUES
    (1, 'Vancouver', 110000, 100000),
    (2, 'Vancouver', 140000, 125000),
    (3, 'Montreal', 150000, 140000),
    (4, 'Montreal', 155000, 146000);

UPDATE store_sales SET net_profit = gross_sales - gross_costs;