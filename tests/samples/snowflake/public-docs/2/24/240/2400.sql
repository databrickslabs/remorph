SELECT site_ID, ts, voltage
    FROM voltage_readings
    WHERE voltage = 0
    ORDER BY ts;