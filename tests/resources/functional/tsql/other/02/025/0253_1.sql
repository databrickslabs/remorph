--Query type: DDL
CREATE TABLE #temp (c_acctbal VARCHAR(50));
EXEC sp_addextendedproperty @name = N'MS_Description', @value = N'The account balance of the customer', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'TABLE', @level1name = N'#temp', @level2type = N'COLUMN', @level2name = N'c_acctbal';
INSERT INTO #temp (c_acctbal) VALUES ('dummy');
SELECT * FROM #temp;
-- REMORPH CLEANUP: DROP TABLE #temp;