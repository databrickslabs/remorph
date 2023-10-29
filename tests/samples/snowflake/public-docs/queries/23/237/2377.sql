-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

select to_timestamp(parse_json(31000000));
select parse_json(31000000)::timestamp_ntz;