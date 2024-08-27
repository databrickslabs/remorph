-- snowflake sql:
select
  varchar1,
  float1::varchar,
  variant1:"Loan Number"::varchar from tmp;

-- revised snowflake sql
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
  CAST(float1 AS STRING),
  CAST(variant1.`Loan Number` AS STRING)
FROM tmp;

-- revised databricks sql
SELECT
  varchar1,
  CAST(float1 AS STRING),
  CAST(variant1.Loan_Number AS STRING)
FROM values (
    'example_varchar',
    123.456,
    named_struct('Loan_Number', 'LN789')
) AS tmp (varchar1, float1, variant1);
