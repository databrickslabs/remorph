select to_timestamp(parse_json(31000000)::int);
select parse_json(31000000)::int::timestamp_ntz;