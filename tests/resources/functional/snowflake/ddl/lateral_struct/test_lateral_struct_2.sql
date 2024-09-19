-- snowflake sql:
SELECT
  f.value:name AS "Contact",
  f.value:first,
  CAST(p.col:a:info:id AS DOUBLE) AS "id_parsed",
  p.col:b:first,
  p.col:a:info
FROM
  (SELECT
    OBJECT_CONSTRUCT(
      'a', OBJECT_CONSTRUCT(
        'info', OBJECT_CONSTRUCT('id', 101, 'first', 'John'),
        'contact', ARRAY_CONSTRUCT(
          OBJECT_CONSTRUCT('name', 'Alice', 'first', 'A'),
          OBJECT_CONSTRUCT('name', 'Bob', 'first', 'B')
        )
      ),
      'b', OBJECT_CONSTRUCT('id', 101, 'first', 'John')
    ) AS col
  ) AS p
, LATERAL FLATTEN(input => p.col:a:contact) AS f;

-- databricks sql:
SELECT
  f.name AS `Contact`,
  f.first,
  CAST(p.col.a.info.id AS DOUBLE) AS `id_parsed`,
  p.col.b.first,
  p.col.a.info
FROM
  (SELECT
    STRUCT(STRUCT(
      STRUCT(101 AS id, 'John' AS first) AS info,
      ARRAY(
        STRUCT('Alice' AS name, 'A' AS first),
        STRUCT('Bob' AS name, 'B' AS first)
      ) AS contact
    ) AS a,
    STRUCT(101 AS id, 'John' AS first) AS b) AS col
  )
AS p
LATERAL VIEW EXPLODE(p.col.a.contact) AS f;