-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

CREATE OR REPLACE TABLE ts_test(ts timestamp_ntz);

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';

INSERT INTO ts_test values('2014-01-01 16:00:00');
INSERT INTO ts_test values('2014-01-02 16:00:00 +00:00');

-- Note that both times from different time zones are converted to the same "wallclock" time

SELECT ts, hour(ts) FROM ts_test;


-- Next, note that changing the session time zone does not influence the results

ALTER SESSION SET TIMEZONE = 'America/New_York';

SELECT ts, hour(ts) FROM ts_test;
