-- see https://docs.snowflake.com/en/sql-reference/classes/forecast

<model_name>!FORECAST(
  INPUT_DATA => <input_data>,
  TIMESTAMP_COLNAME => '<timestamp_colname>',
  [CONFIG_OBJECT => <config_object>]
);