-- snowflake sql:
SELECT
  p.info:id AS `ID`,
  p.info:first AS `First`,
  p.info:first.b AS C
FROM (
  SELECT
    PARSE_JSON('{"id": {"a":{"c":"102","d":"106"}}, "first": {"b":"105"}}')
) AS p(info);

-- databricks sql:
SELECT
  p.col:a.info,
  CAST(p.col:a:info:id AS DOUBLE) AS `id_parsed`,
  p.col:b:first,
  p.col:a:info
FROM (
  SELECT
    PARSE_JSON(
      '{\n        "a": {\n          "info": {"id": 101, "first": "John"},\n          "contact": [\n            {"name": "Alice", "first": "A"},\n            {"name": "Bob", "first": "B"}\n          ]\n        },\n        "b": {"id": 101, "first": "John"}\n      }'
    )
) AS p(col)
