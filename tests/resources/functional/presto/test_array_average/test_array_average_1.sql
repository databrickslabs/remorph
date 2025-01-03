-- presto sql:
select
  id,
  sum(array_average(arr)) as sum_arr
FROM
  (
    SELECT
      1 as id,
      ARRAY [1,2,3] AS arr
    UNION
    SELECT
      2 as id,
      ARRAY [10.20,20.108,30.4,40.0] as arr
  ) AS t
group by
  id;

-- databricks sql:
SELECT
  id,
  SUM(
    AGGREGATE(
      FILTER(arr, x -> x IS NOT NULL),
      NAMED_STRUCT('sum', CAST(0 AS DOUBLE), 'cnt', 0),
      (acc, x) -> NAMED_STRUCT('sum', acc.sum + x, 'cnt', acc.cnt + 1),
      acc -> TRY_DIVIDE(acc.sum, acc.cnt)
    )
  ) AS sum_arr
FROM
  (
    SELECT
      1 AS id,
      ARRAY(1, 2, 3) AS arr
    UNION
    SELECT
      2 AS id,
      ARRAY(10.20, 20.108, 30.4, 40.0) AS arr
  ) AS t
GROUP BY
  id;
