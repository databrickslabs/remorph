-- tsql sql:
CREATE TABLE orders (o_orderkey INT PRIMARY KEY, o_comment VARCHAR(100) SPARSE NULL, o_custkey INT SPARSE NULL, OSet XML COLUMN_SET FOR ALL_SPARSE_COLUMNS); -- REMORPH CLEANUP: DROP TABLE orders;