-- see https://docs.snowflake.com/en/sql-reference/functions/conditional_change_event

WITH power_change_events AS
    (
    SELECT
          site_ID,
          CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
        FROM voltage_readings
    )
SELECT MAX(power_changes) 
    FROM power_change_events
    GROUP BY site_ID
    ;