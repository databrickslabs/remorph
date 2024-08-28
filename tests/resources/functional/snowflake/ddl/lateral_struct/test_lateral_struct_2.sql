-- snowflake sql:
SELECT
  f.value:name AS "Contact",
  f.value:first,
  CAST(p.value:a:value:id AS DOUBLE) AS "id_parsed",
  p.value:b:first,
  p.value:a:value
FROM
  (SELECT
    OBJECT_CONSTRUCT(
      'a', OBJECT_CONSTRUCT(
        'value', OBJECT_CONSTRUCT('id', 101, 'first', 'John'),
        'contact', ARRAY_CONSTRUCT(
          OBJECT_CONSTRUCT('name', 'Alice', 'first', 'A'),
          OBJECT_CONSTRUCT('name', 'Bob', 'first', 'B')
        )
      ),
      'b', OBJECT_CONSTRUCT('id', 101, 'first', 'John')
    ) AS value
  ) AS p
, LATERAL FLATTEN(input => p.value:a:contact) AS f;

-- databricks sql:
SELECT
  f.name AS `Contact`,
  f.first,
  CAST(p.a.value.id AS DOUBLE) AS `id_parsed`,
  p.b.first,
  p.a.value
FROM
  (SELECT
    STRUCT(
      STRUCT(101 AS id, 'John' AS first) AS value,
      ARRAY(
        STRUCT('Alice' AS name, 'A' AS first),
        STRUCT('Bob' AS name, 'B' AS first)
      ) AS contact
    ) AS c,
    STRUCT(101 AS id, 'John' AS first) AS value
  )
AS p(a,b)
Lateral VIEW EXPLODE(p.a.contact) AS f