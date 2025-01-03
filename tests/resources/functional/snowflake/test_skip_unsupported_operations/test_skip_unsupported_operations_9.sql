
-- snowflake sql:

                CREATE TASK t1
                  SCHEDULE = '30 MINUTE'
                  TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24'
                  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
                AS
                INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
                ;

-- databricks sql:
-- CREATE TASK t1 SCHEDULE = '30 MINUTE' TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24' USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' AS INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
