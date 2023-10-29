-- see https://docs.snowflake.com/en/sql-reference/functions/external_functions_history

select *
  from table(information_schema.external_functions_history(
    date_range_start => dateadd('day', -14, current_date()),
    date_range_end => current_date(),
    function_signature => 'mydb.public.myfunction(integer, varchar)'));