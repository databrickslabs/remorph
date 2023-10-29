-- see https://docs.snowflake.com/en/sql-reference/functions/system_clustering_information

SELECT SYSTEM$CLUSTERING_INFORMATION('t1', 5);