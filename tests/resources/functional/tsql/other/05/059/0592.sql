-- tsql sql:
CREATE TABLE #temp (id INT);
CREATE INDEX IX_ORDERS_INDEX ON #temp (id);
ALTER INDEX IX_ORDERS_INDEX ON #temp REBUILD WITH (XML_COMPRESSION = ON);
SELECT * FROM #temp;
-- REMORPH CLEANUP: DROP TABLE #temp;
