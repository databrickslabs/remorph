-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

select '2021-01-01 00:00:00 +0000'::timestamp_tz = '2021-01-01 01:00:00 +0100'::timestamp_tz;