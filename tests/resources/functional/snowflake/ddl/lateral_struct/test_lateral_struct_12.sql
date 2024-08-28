-- snowflake sql:
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
 FROM
   (
     select ARRAY_CONSTRUCT('value1', 'value2', 'value3') as value
   ) AS sample_data(array_column),
   LATERAL FLATTEN(input => sample_data.array_column, OUTER => true) AS verticals;

