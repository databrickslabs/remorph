-- presto sql:
SELECT
  any_keys_match(
    map(array ['a', 'b', 'c'], array [1, 2, 3]),
    x -> x = 'a'
  ) as col;

-- databricks sql:
SELECT
  EXISTS(
    MAP_KEYS(
      MAP_FROM_ARRAYS(ARRAY('a', 'b', 'c'), ARRAY(1, 2, 3))
    ),
    x -> x = 'a'
  ) AS col;
