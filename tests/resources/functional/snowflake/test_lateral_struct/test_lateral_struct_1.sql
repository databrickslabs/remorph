
-- source:
SELECT p.value:id as "ID" FROM persons_struct p;

-- databricks_sql:
SELECT p.value.id AS `ID` FROM persons_struct AS p;
