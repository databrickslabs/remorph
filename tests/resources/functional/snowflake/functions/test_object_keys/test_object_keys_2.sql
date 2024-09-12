-- snowflake sql:
SELECT OBJECT_KEYS (
       PARSE_JSON (
           column1
           )
       ) AS keys
FROM table
ORDER BY 1;
;

-- databricks sql:
SELECT JSON_OBJECT_KEYS ( FROM_JSON ( column1, SCHEMA_OF_JSON ( '{column1_schema}' )  )  ) AS keys FROM table ORDER BY 1 nulls LAST;


-- experimental sql:
SELECT JSON_OBJECT_KEYS(PARSE_JSON(column1)) AS keys FROM table ORDER BY 1 NULLS LAST;