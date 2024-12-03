--Query type: DDL
DECLARE @max_cpu_percent DECIMAL(5, 2);
DECLARE @max_memory_percent DECIMAL(5, 2);

WITH resource_pool AS (
    SELECT 50 AS max_cpu_percent, 25 AS max_memory_percent
)
-- Select the values into the variables
SELECT @max_cpu_percent = max_cpu_percent, @max_memory_percent = max_memory_percent
FROM resource_pool;

-- Create a table to demonstrate the use of variables in DML
CREATE TABLE #resource_config (
    max_cpu_percent DECIMAL(5, 2),
    max_memory_percent DECIMAL(5, 2)
);

-- Insert values into the table
INSERT INTO #resource_config (max_cpu_percent, max_memory_percent)
VALUES (@max_cpu_percent, @max_memory_percent);

-- Select the data from the table
SELECT * FROM #resource_config;

-- REMORPH CLEANUP: DROP TABLE #resource_config;
