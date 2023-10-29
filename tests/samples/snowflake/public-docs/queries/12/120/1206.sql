-- see https://docs.snowflake.com/en/sql-reference/functions/hll_export

SELECT HLL(o_orderdate), HLL_ESTIMATE(HLL_IMPORT(HLL_EXPORT(HLL_ACCUMULATE(o_orderdate))))
FROM orders;
