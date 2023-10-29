-- see https://docs.snowflake.com/en/sql-reference/literals-table

SELECT * FROM TABLE('mydb."myschema"."mytable"');

SELECT * FROM TABLE($$mydb."myschema"."mytable"$$);