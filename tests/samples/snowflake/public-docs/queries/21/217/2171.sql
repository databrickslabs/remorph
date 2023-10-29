-- see https://docs.snowflake.com/en/sql-reference/functions/is

select * from vartab where is_null_value(v);


select * from vartab where is_boolean(v);


select * from vartab where is_integer(v);


select * from vartab where is_decimal(v);


select * from vartab where is_double(v);


select * from vartab where is_varchar(v);


select * from vartab where is_array(v);


select * from vartab where is_object(v);
