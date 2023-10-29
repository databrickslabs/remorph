-- see https://docs.snowflake.com/en/sql-reference/classes/forecast

CREATE SNOWFLAKE.ML.FORECAST <name>(
  '<input_data>', '<series_colname>', '<timestamp_colname>', '<target_colname>');