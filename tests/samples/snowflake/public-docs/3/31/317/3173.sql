col1 varchar as (parse_json(metadata$external_table_partition):col1::varchar),
col2 number as (parse_json(metadata$external_table_partition):col2::number),
col3 timestamp_tz as (parse_json(metadata$external_table_partition):col3::timestamp_tz)