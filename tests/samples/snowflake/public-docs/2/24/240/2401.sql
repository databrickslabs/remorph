SELECT
      site_ID,
      ts,
      voltage,
      CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
    FROM voltage_readings;