USE DATABASE mydb;

SELECT table_name, last_load_time
  FROM information_schema.load_history
  WHERE schema_name=current_schema() AND
  table_name='MYTABLE' AND
  last_load_time > 'Fri, 01 Apr 2016 16:00:00 -0800';