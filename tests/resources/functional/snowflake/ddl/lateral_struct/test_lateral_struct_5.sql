-- snowflake sql:
SELECT
  varchar1,
  CAST(float1 AS STRING) AS float1_as_string,
  CAST(variant1:Loan_Number AS STRING) AS loan_number_as_string
FROM
  (SELECT
    'example_varchar' AS varchar1,
    123.456 AS float1,
    OBJECT_CONSTRUCT('Loan_Number', 'LN789') AS variant1
  ) AS tmp;

-- databricks sql:
SELECT
  varchar1,
  CAST(float1 AS STRING) as float1_as_string,
  CAST(variant1.Loan_Number AS STRING) as loan_number_as_string
FROM (
  SELECT
    'example_varchar' AS varchar1,
    123.456 AS float1,
    STRUCT('LN789' AS Loan_Number) AS variant1
) AS tmp;
