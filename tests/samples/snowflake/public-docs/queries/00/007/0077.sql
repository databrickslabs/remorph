-- see https://docs.snowflake.com/en/sql-reference/classes/forecast

<model_name>!FORECAST(
  SERIES_VALUE => <series>,
  FORECASTING_PERIODS => <forecasting_periods>,
  TIMESTAMP_COLNAME => '<timestamp_colname>',
  [CONFIG_OBJECT => <config_object>]
);