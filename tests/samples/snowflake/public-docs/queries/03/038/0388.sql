-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

CREATE OR REPLACE TABLE ts_test(ts timestamp_ltz);

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

INSERT INTO ts_test values('2014-01-01 16:00:00');
INSERT INTO ts_test values('2014-01-02 16:00:00 +00:00');

-- Note that the time for January 2nd is 08:00 in Los Angeles (which is 16:00 in UTC)

SELECT ts, hour(ts) FROM ts_test;


-- Next, note that the times change with a different time zone

ALTER SESSION SET TIMEZONE = 'America/New_York';

SELECT ts, hour(ts) FROM ts_test;
