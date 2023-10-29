-- see https://docs.snowflake.com/en/sql-reference/functions/split

SELECT * FROM persons;


SELECT name, C.value::string AS childName
FROM persons,
     LATERAL FLATTEN(input=>split(children, ',')) C;
