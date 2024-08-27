-- snowflake sql:
SELECT p.value:id as "ID" FROM persons_struct p;

-- revised snowflake sql
SELECT
    p.value:id AS "ID"
FROM
    (SELECT OBJECT_CONSTRUCT('id', 102, 'first', 'Jane') AS value) AS p;


-- databricks sql:
SELECT p.value.id AS `ID` FROM persons_struct AS p;


--revised databricks sql
SELECT
    p.value.id AS `ID`
FROM
    (SELECT STRUCT(102 AS id, 'Jane' AS first) AS value) AS p;