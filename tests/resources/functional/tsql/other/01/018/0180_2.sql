--Query type: DDL
CREATE TABLE #temp (c5 VARCHAR(50));
INSERT INTO #temp (c5) VALUES ('50 character column');
EXEC sp_addextendedproperty @name = N'MS_Description', @value = '50 character column', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'#temp', @level2type = N'COLUMN', @level2name = N'c5';
SELECT c5 FROM #temp;
-- REMORPH CLEANUP: DROP TABLE #temp;
