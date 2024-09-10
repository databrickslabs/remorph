-- snowflake sql:
SELECT OBJECT_CONSTRUCT('Key_One', PARSE_JSON('NULL'), 'Key_Two', NULL, 'Key_Three', 'null') as obj;

-- databricks sql:
SELECT STRUCT( FROM_JSON ( 'null', SCHEMA_OF_JSON ( '{json_column}' )  ) AS key_one, null AS key_two, 'null' AS key_three ) as obj

-- experimental sql:
SELECT STRUCT(PARSE_JSON('NULL') AS Key_One, NULL AS Key_Two, 'null' AS Key_Three) AS obj;
