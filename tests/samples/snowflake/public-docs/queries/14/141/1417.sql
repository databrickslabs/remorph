-- see https://docs.snowflake.com/en/sql-reference/functions/system_clustering_ratio

SELECT SYSTEM$CLUSTERING_RATIO('t2', '(col1, col3)');
