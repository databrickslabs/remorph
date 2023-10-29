-- see https://docs.snowflake.com/en/sql-reference/parameters

alter session set TIMESTAMP_DAY_IS_ALWAYS_24H = true;

-- With DST beginning on 2018-03-11 at 2 AM, America/Los_Angeles time zone
select dateadd(day, 1, '2018-03-10 09:00:00'::TIMESTAMP_LTZ), dateadd(day, 1, '2018-11-03 09:00:00'::TIMESTAMP_LTZ);


alter session set TIMESTAMP_DAY_IS_ALWAYS_24H = false;

select dateadd(day, 1, '2018-03-10 09:00:00'::TIMESTAMP_LTZ), dateadd(day, 1, '2018-11-03 09:00:00'::TIMESTAMP_LTZ);
