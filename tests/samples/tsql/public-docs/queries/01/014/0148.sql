-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-recommendations-sql?view=azure-sqldw-latest

-- Step 1: Turn the distribution advisor ON for the current client session
SET RECOMMENDATIONS ON;
GO

-- <insert your queries here, up to 100>
SELECT ss_store_sk, COUNT(*) FROM store_sales, store WHERE ss_store_sk = s_store_sk GROUP BY ss_store_sk;

SELECT cs_item_sk, COUNT(*) FROM catalog_sales, item WHERE cs_item_sk = i_item_sk  AND i_manufact_id > 100 GROUP BY cs_item_sk;

SELECT * FROM dbo.reason;

-- Turn the distribution advisor OFF for the current client session.
SET RECOMMENDATIONS OFF;
GO