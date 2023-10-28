select * from table(validate_pipe_load(
  pipe_name=>'MY_DB.PUBLIC.MYPIPE',
  start_time=>dateadd(hour, -1, current_timestamp())));