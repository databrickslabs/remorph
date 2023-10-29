-- see https://docs.snowflake.com/en/sql-reference/functions/conditional_change_event

SELECT site_ID, ts, voltage
    FROM voltage_readings
    WHERE voltage = 0
    ORDER BY ts;