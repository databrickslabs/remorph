-- see https://docs.snowflake.com/en/sql-reference/functions/conditional_change_event

SELECT
      site_ID,
      ts,
      voltage,
      CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
    FROM voltage_readings;