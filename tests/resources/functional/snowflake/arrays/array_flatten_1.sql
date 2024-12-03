-- snowflake sql:
SELECT
  ARRAY_FLATTEN([[1, 2, 3], [4], [5, 6]]) as col
, ARRAY_FLATTEN([[[1, 2], [3]], [[4], [5]]]) as col1
, ARRAY_FLATTEN([[1, 2, 3], NULL, [5, 6]]) as col3;

-- databricks sql:
select
  flatten(array(array(1, 2, 3) , array(4) , array(5, 6))) as col,
  flatten(array(array(array(1, 2) , array(3)) , array(array(4) , array(5)))) as col1,
  flatten(array(array(1, 2, 3) , null, array(5, 6))) as col3;
