-- presto sql:
SELECT
  json_size(col, path) as j_size,
  id
from
  (
    select
      '{"x": {"a": 1, "b": 2}}' as col,
      '$.x' as path,
      1 as id
    union
    select
      '{"x": [1, 2, 3]}' as col,
      '$.x' as path,
      2 as id
    union
    select
      '{"x": {"a": 1, "b": 2}}' as col,
      '$.x.a' as path,
      3 as id
    union
    select
      '42' as col,
      '$' as path,
      4 as id
    union
    select
      'invalid json' as col,
      '$' as path,
      5 as id
  ) tmp
order by
  id;

-- databricks sql:
SELECT
  CASE
    WHEN GET_JSON_OBJECT(col, path) LIKE '{%' THEN SIZE(
      FROM_JSON(GET_JSON_OBJECT(col, path), 'map<string,string>')
    )
    WHEN GET_JSON_OBJECT(col, path) LIKE '[%' THEN SIZE(
      FROM_JSON(GET_JSON_OBJECT(col, path), 'array<string>')
    )
    WHEN GET_JSON_OBJECT(col, path) IS NOT NULL THEN 0
    ELSE NULL
  END AS j_size,
  id
from
  (
    select
      '{"x": {"a": 1, "b": 2}}' as col,
      '$.x' as path,
      1 as id
    union
    select
      '{"x": [1, 2, 3]}' as col,
      '$.x' as path,
      2 as id
    union
    select
      '{"x": {"a": 1, "b": 2}}' as col,
      '$.x.a' as path,
      3 as id
    union
    select
      '42' as col,
      '$' as path,
      4 as id
    union
    select
      'invalid json' as col,
      '$' as path,
      5 as id
  ) as tmp
order by
  id nulls last;
