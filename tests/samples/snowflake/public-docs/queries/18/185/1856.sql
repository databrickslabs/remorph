-- see https://docs.snowflake.com/en/sql-reference/functions/getvariable

SET MY_LOCAL_VARIABLE= 'my_local_variable_value';
SELECT 
    GETVARIABLE('MY_LOCAL_VARIABLE'), 
    SESSION_CONTEXT('MY_LOCAL_VARIABLE'),
    $MY_LOCAL_VARIABLE;