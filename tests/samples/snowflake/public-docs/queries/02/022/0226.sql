-- see https://docs.snowflake.com/en/sql-reference/snowflake-db-classes

CALL my_anomaly_detector!DETECT_ANOMALIES(
  INPUT_DATA => SYSTEM$REFERENCE('VIEW', '<view_name>'),
  TIMESTAMP_COLNAME =>'<timestamp_column_name>',
  TARGET_COLNAME => '<target_column_name>'
);