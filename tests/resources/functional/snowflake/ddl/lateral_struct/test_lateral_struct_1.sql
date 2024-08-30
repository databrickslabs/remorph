-- snowflake sql:
SELECT
    p.info:id AS "ID"
FROM
    (SELECT OBJECT_CONSTRUCT('id', 102, 'first', 'Jane') AS info) AS p;

-- databricks sql:
SELECT
    p.info.id AS `ID`
FROM
    (SELECT STRUCT(102 AS id, 'Jane' AS first) AS info) AS p;