--Query type: DML
-- Create tables
CREATE TABLE customers
(
    c_custkey INT,
    c_name VARCHAR(255),
    c_address VARCHAR(255),
    c_nationkey INT
);

CREATE TABLE orders
(
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus VARCHAR(255),
    o_totalprice DECIMAL(10, 2)
);

-- Create target table
CREATE TABLE target
(
    k INT,
    v DECIMAL(10, 2)
);

-- Create CTE
WITH src AS (
    SELECT c_custkey AS k, o_totalprice AS v
    FROM customers
    INNER JOIN orders ON c_custkey = o_custkey
)
-- MERGE query
MERGE target AS t
USING (
    SELECT k, MAX(v) AS v
    FROM src
    GROUP BY k
) AS b
ON t.k = b.k
WHEN MATCHED THEN
    UPDATE SET t.v = b.v
WHEN NOT MATCHED THEN
    INSERT (k, v)
    VALUES (b.k, b.v);

-- SELECT statement
SELECT * FROM target;

-- REMORPH CLEANUP: DROP TABLE customers;
-- REMORPH CLEANUP: DROP TABLE orders;
-- REMORPH CLEANUP: DROP TABLE target;