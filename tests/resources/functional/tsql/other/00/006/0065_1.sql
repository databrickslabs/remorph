-- tsql sql:
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'daily_revenue')
CREATE TABLE daily_revenue (
    id INT,
    category VARCHAR(50),
    sales DECIMAL(10, 2),
    profit DECIMAL(10, 2),
    expenses DECIMAL(10, 2),
    tax DECIMAL(10, 2)
);

INSERT INTO daily_revenue (id, category, sales, profit, expenses, tax)
SELECT id, category, sales, profit, expenses, tax
FROM (VALUES
    (1, 'food', 500.00, 200.00, 150.00, 50.00),
    (2, 'beverages', 300.00, 100.00, 75.00, 25.00),
    (3, 'snacks', 200.00, 50.00, 25.00, 10.00)
) AS temp_result(id, category, sales, profit, expenses, tax);

SELECT * FROM daily_revenue;

-- REMORPH CLEANUP: DROP TABLE daily_revenue;
