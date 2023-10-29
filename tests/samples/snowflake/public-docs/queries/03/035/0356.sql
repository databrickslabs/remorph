-- see https://docs.snowflake.com/en/sql-reference/functions/lead

CREATE OR REPLACE TABLE sales(emp_id INTEGER, year INTEGER, revenue DECIMAL(10,2));
INSERT INTO sales VALUES (0, 2010, 1000), (0, 2011, 1500), (0, 2012, 500), (0, 2013, 750);
INSERT INTO sales VALUES (1, 2010, 10000), (1, 2011, 12500), (1, 2012, 15000), (1, 2013, 20000);
INSERT INTO sales VALUES (2, 2012, 500), (2, 2013, 800);

SELECT emp_id, year, revenue, LEAD(revenue) OVER (PARTITION BY emp_id ORDER BY year) - revenue AS diff_to_next FROM sales ORDER BY emp_id, year;
