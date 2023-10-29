-- see https://docs.snowflake.com/en/sql-reference/functions/approx_top_k

SELECT APPROX_TOP_K(C4) FROM lineitem;
