
-- presto sql:
SELECT CASE WHEN strpos(greeting_message, 'hello') > 0 THEN 'Contains hello' ELSE 'Does not contain hello' END FROM greetings_table;;

-- databricks sql:
SELECT CASE WHEN LOCATE(greeting_message, 'hello') > 0 THEN 'Contains hello' ELSE 'Does not contain hello' END FROM greetings_table;
