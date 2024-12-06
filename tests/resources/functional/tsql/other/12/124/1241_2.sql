-- tsql sql:
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TempResult')
CREATE TABLE TempResult (
    c_custkey INT,
    c_name VARCHAR(50),
    o_orderkey VARCHAR(20) DEFAULT 'TPC-H_'
);

WITH DataToInsert AS (
    SELECT c_custkey, c_name, CAST(NEXT VALUE FOR order_seq AS NVARCHAR(20)) AS o_orderkey
    FROM your_table
)
INSERT INTO TempResult (c_custkey, c_name, o_orderkey)
SELECT c_custkey, c_name, o_orderkey
FROM DataToInsert;

SELECT * FROM TempResult;
-- REMORPH CLEANUP: DROP TABLE TempResult;
