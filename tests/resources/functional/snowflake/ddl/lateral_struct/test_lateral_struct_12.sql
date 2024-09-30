-- snowflake sql:
SELECT
   verticals.index AS index,
   verticals.value AS array_val
 FROM
   (
     select ARRAY_CONSTRUCT('value1', 'value2', 'value3') as col
   ) AS sample_data(array_column),
   LATERAL FLATTEN(input => sample_data.array_column, OUTER => true) AS verticals;

-- databricks sql:
SELECT
  verticals.index AS index,
  verticals.value AS array_val
FROM (
  SELECT
    ARRAY('value1', 'value2', 'value3') AS col
) AS sample_data(array_column)
 LATERAL VIEW OUTER POSEXPLODE(sample_data.array_column) verticals AS index, value;
