-- tsql sql:
CREATE TABLE #Supplier (s_suppkey INT, s_name VARCHAR(255), s_address VARCHAR(255));
INSERT INTO #Supplier (s_suppkey, s_name, s_address)
SELECT s_suppkey, s_name, s_address
FROM (
    VALUES (1, 'Supplier#000000001', '123 Main St'),
           (2, 'Supplier#000000002', '456 Elm St')
) AS T (s_suppkey, s_name, s_address);
CREATE NONCLUSTERED INDEX ncci ON #Supplier (s_suppkey, s_name, s_address);
SELECT * FROM #Supplier;
-- REMORPH CLEANUP: DROP TABLE #Supplier;
-- REMORPH CLEANUP: DROP INDEX ncci ON #Supplier;
