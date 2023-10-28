-- example setup
CREATE OR REPLACE TABLE monthly_sales(empid INT, dept TEXT, jan INT, feb INT, mar INT, april INT);

INSERT INTO monthly_sales VALUES
    (1, 'electronics', 100, 200, 300, 100),
    (2, 'clothes', 100, 300, 150, 200),
    (3, 'cars', 200, 400, 100, 50);

-- UNPIVOT example
SELECT * FROM monthly_sales
    UNPIVOT(sales FOR month IN (jan, feb, mar, april))
    ORDER BY empid;
