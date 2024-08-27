-- snowflake sql:
SELECT
  verticals.index AS index,
  verticals.value AS value
FROM
  sample_data,
  LATERAL FLATTEN(input => array_column, OUTER => true ) AS verticals;

 -- revised snowflake sql:
 SELECT
   verticals.index AS index,
   verticals.value AS value
 FROM
   (
     select ARRAY_CONSTRUCT('value1', 'value2', 'value3') as value
   ) AS sample_data(array_column),
   LATERAL FLATTEN(input => sample_data.array_column, OUTER => true) AS verticals;


-- databricks sql:
SELECT
  verticals.index AS index,
  verticals.value AS value
FROM sample_data
  LATERAL VIEW OUTER POSEXPLODE(array_column) verticals AS index, value;

 -- revised databricks sql:
 SELECT
   verticals.index AS index,
   verticals.value AS value
 FROM
   (
     select ARRAY_CONSTRUCT('value1', 'value2', 'value3') as value
   ) AS sample_data(array_column),
   LATERAL FLATTEN(input => sample_data.array_column, OUTER => true) AS verticals;

