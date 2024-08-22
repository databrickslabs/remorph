-- snowflake sql:
SELECT
  verticals.index AS index,
  verticals.value AS value
FROM
  sample_data,
  LATERAL FLATTEN(input => array_column, OUTER => true ) AS verticals;

-- databricks sql:
SELECT
  verticals.index AS index,
  verticals.value AS value
FROM sample_data
  LATERAL VIEW OUTER POSEXPLODE(array_column) verticals AS index, value;
