CREATE TABLE voltage_readings (
    site_ID INTEGER, -- which refrigerator the measurement was taken in.
    ts TIMESTAMP,  -- the time at which the temperature was measured.
    VOLTAGE FLOAT
    );
INSERT INTO voltage_readings (site_ID, ts, voltage) VALUES
    (1, '2019-10-30 13:00:00', 120),
    (1, '2019-10-30 13:15:00', 120),
    (1, '2019-10-30 13:30:00',   0),
    (1, '2019-10-30 13:45:00',   0),
    (1, '2019-10-30 14:00:00',   0),
    (1, '2019-10-30 14:15:00',   0),
    (1, '2019-10-30 14:30:00', 120)
    ;