-- see https://docs.snowflake.com/en/sql-reference/functions/try_to_boolean

SELECT TRY_TO_BOOLEAN('True')  AS "T", 
       TRY_TO_BOOLEAN('False') AS "F",
       TRY_TO_BOOLEAN('Oops')  AS "N";