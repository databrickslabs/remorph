begin transaction;

create table parent(id integer);
create table child (child_id integer, parent_ID integer);

-- ----------------------------------------------------- --
-- Wrap multiple related statements in a transaction,
-- and use try/catch to commit or roll back.
-- ----------------------------------------------------- --
-- Create the procedure
create or replace procedure cleanup(FORCE_FAILURE varchar)
  returns varchar not null
  language javascript
  as
  $$
  var result = "";
  snowflake.execute( {sqlText: "begin transaction;"} );
  try {
      snowflake.execute( {sqlText: "delete from child where parent_id = 1;"} );
      snowflake.execute( {sqlText: "delete from parent where id = 1;"} );
      if (FORCE_FAILURE === "fail")  {
          // To see what happens if there is a failure/rollback,
          snowflake.execute( {sqlText: "delete from no_such_table;"} );
          }
      snowflake.execute( {sqlText: "commit;"} );
      result = "Succeeded";
      }
  catch (err)  {
      snowflake.execute( {sqlText: "rollback;"} );
      return "Failed: " + err;   // Return a success/error indicator.
      }
  return result;
  $$
  ;

commit;