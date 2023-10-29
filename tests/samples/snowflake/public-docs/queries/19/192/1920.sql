-- see https://docs.snowflake.com/en/sql-reference/info-schema/load_history

USE DATABASE mydb;

SELECT table_name, last_load_time
  FROM information_schema.load_history
  ORDER BY last_load_time DESC
  LIMIT 10;