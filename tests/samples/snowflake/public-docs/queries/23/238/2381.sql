-- see https://docs.snowflake.com/en/sql-reference/functions/to_char

select to_varchar('2013-04-05 01:02:03'::timestamp, 'mm/dd/yyyy, hh24:mi hours');
