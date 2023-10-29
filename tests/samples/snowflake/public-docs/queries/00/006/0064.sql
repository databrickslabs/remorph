-- see https://docs.snowflake.com/en/sql-reference/functions/system_set_return_value

-- create a table to store the return values.
create or replace table return_values_sp (str varchar);

-- create a stored procedure that sets the return value for the task.
create or replace procedure set_return_value_sp()
returns string
language javascript
execute as caller
as $$
  var stmt = snowflake.createStatement({sqlText:`call system$set_return_value('The quick brown fox jumps over the lazy dog');`});
  var res = stmt.execute();
$$;

-- create a stored procedure that inserts the return value for the predecessor task into the 'return_values_sp' table.
create or replace procedure get_return_value_sp()
returns string
language javascript
execute as caller
as $$
var stmt = snowflake.createStatement({sqlText:`insert into return_values_sp values(system$get_predecessor_return_value());`});
var res = stmt.execute();
$$;

-- create a task that calls the set_return_value stored procedure.
create task set_return_value_t
warehouse=warehouse1
schedule='1 minute'
as
  call set_return_value_sp();

-- create a task that calls the get_return_value stored procedure.
create task get_return_value_t
warehouse=warehouse1
after set_return_value_t
as
  call get_return_value_sp();

-- resume task.
-- wait for task to run on schedule.

select distinct(str) from return_values_sp;

select distinct(RETURN_VALUE)
  from table(information_schema.task_history())
  where RETURN_VALUE is not NULL;
