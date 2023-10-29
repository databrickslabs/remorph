-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';
SELECT TO_TIMESTAMP_TZ('2013-04-05 01:02:03');

SELECT TO_TIMESTAMP_NTZ('2013-04-05 01:02:03');