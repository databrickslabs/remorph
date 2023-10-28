SELECT column1 timestamp_1, column2 timestamp_2,
      DATEDIFF(hour, column1, column2) diff_hours,
      DATEDIFF(minute, column1, column2) diff_minutes,
      DATEDIFF(second, column1, column2) diff_seconds
    FROM VALUES
      ('2016-01-01 01:59:59'::TIMESTAMP, '2016-01-01 02:00:00'::TIMESTAMP),
      ('2016-01-01 01:00:00'::TIMESTAMP, '2016-01-01 01:59:00'::TIMESTAMP),
      ('2016-01-01 01:00:59'::TIMESTAMP, '2016-01-01 02:00:00'::TIMESTAMP);