-- see https://docs.snowflake.com/en/sql-reference/functions/system_clustering_depth

SELECT SYSTEM$CLUSTERING_DEPTH('TPCH_ORDERS', '(C2, C9)', 'C2 = 25');
