-- see https://docs.snowflake.com/en/sql-reference/functions/system_clustering_information

SELECT SYSTEM$CLUSTERING_INFORMATION('test2', '(col1, col3)');