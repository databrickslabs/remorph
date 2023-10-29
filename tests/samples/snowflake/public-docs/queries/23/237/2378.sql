-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

select to_timestamp(parse_json(31000000)::int);
select parse_json(31000000)::int::timestamp_ntz;