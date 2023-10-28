select *
  from table(information_schema.external_functions_history(
    function_signature => 'mydb.public.myfunction(integer, varchar)'));