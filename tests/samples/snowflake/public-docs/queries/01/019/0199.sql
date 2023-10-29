-- see https://docs.snowflake.com/en/sql-reference/functions/is_time

BEGIN WORK;
insert into vardttm select to_variant(to_date('2017-02-24'));
insert into vardttm select to_variant(to_time('20:57:01.123456789+07:00'));
insert into vardttm select to_variant(to_timestamp('2017-02-24 12:00:00.456'));
insert into vardttm select to_variant(to_timestamp_ltz('2017-02-24 13:00:00.123 +01:00'));
insert into vardttm select to_variant(to_timestamp_ntz('2017-02-24 14:00:00.123 +01:00'));
insert into vardttm select to_variant(to_timestamp_tz('2017-02-24 15:00:00.123 +01:00'));
COMMIT WORK;