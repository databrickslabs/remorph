-- see https://docs.snowflake.com/en/sql-reference/snowflake-db-classes

GRANT SNOWFLAKE.ML.ANOMALY_DETECTION ROLE my_db.my_schema.my_anomaly_detector!USER
  TO ROLE my_role;