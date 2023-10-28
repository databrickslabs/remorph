USE DATABASE mydb;

SELECT table_name, last_load_time
  FROM information_schema.load_history
  ORDER BY last_load_time DESC
  LIMIT 10;