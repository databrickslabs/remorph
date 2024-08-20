-- snowflake sql:
SELECT p.value:id as "ID" FROM persons_struct p;

-- databricks sql:
SELECT p.value.id AS `ID` FROM persons_struct AS p;
