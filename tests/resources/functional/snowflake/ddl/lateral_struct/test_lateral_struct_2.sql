-- snowflake sql:
SELECT
  f.value:name AS "Contact",
  f.value:first,
  CAST(p.col:a:info:id AS DOUBLE) AS "id_parsed",
  p.col:b:first,
  p.col:a:info
FROM
  (SELECT
    PARSE_JSON('{"a": {"info": {"id": 101, "first": "John" }, "contact": [{"name": "Alice", "first": "A"}, {"name": "Bob", "first": "B"}]}, "b": {"id": 101, "first": "John"}}')
  ) AS p(col)
, LATERAL FLATTEN(input => p.col:a:contact) AS f;

-- databricks sql:
SELECT
  f.value:name AS `Contact`,
  f.value:first,
  CAST(p.col:a.info.id AS DOUBLE) AS `id_parsed`,
  p.col:b.first,
  p.col:a.info
FROM (
  SELECT
   PARSE_JSON('{"a": {"info": {"id": 101, "first": "John" }, "contact": [{"name": "Alice", "first": "A"}, {"name": "Bob", "first": "B"}]}, "b": {"id": 101, "first": "John"}}')
) AS p(col)
, LATERAL VARIANT_EXPLODE(p.col:a.contact) AS f;
