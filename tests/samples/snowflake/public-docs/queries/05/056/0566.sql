-- see https://docs.snowflake.com/en/sql-reference/functions/system_current_user_task_name

CREATE TASK mytask
  WAREHOUSE = mywh,
  SCHEDULE = '5 MINUTE'
AS
  INSERT INTO mytable(ts, task) VALUES(CURRENT_TIMESTAMP, SYSTEM$CURRENT_USER_TASK_NAME());

SELECT * FROM mytable;
