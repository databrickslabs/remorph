CREATE ANOMALY_DETECTION <my_anomaly_detector_name>(
  INPUT_DATA => SYSTEM$REFERENCE('VIEW', '<view_with_training_data>'),
  TIMESTAMP_COLUMN => '<timestamp_column_name>'
  TARGET_COLNAME => '<target_column_name>',
  LABEL_COLNAME => ''
);