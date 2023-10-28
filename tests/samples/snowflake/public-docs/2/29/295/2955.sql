CREATE [ OR REPLACE ] SNOWFLAKE.ML.ANOMALY_DETECTION <name>(
  [ SERIES_COLNAME => '<series_column_name>' , ]
  INPUT_DATA => <reference_to_training_data>,
  TIMESTAMP_COLNAME => '<timestamp_column_name>',
  TARGET_COLNAME => '<target_column_name>',
  LABEL_COLNAME => '<label_column_name>'
)