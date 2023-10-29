-- see https://docs.snowflake.com/en/sql-reference/classes/forecast

<model_name>!FORECAST(
  FORECASTING_PERIODS => <forecasting_periods>,
  [CONFIG_OBJECT => <config_object>]
);