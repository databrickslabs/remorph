-- see https://docs.snowflake.com/en/sql-reference/collation

CREATE OR REPLACE TABLE collation_precedence_example2(
  s1 STRING COLLATE '',
  s2 STRING COLLATE 'utf8',
  s3 STRING COLLATE 'fr'
);

-- Uses 'utf8' because s1 has no collation and 'utf8' is the default.
SELECT * FROM collation_precedence_example2 WHERE s1 = 'a';

-- Uses 'utf8' because s1 has no collation and s2 has explicit 'utf8' collation.
SELECT * FROM collation_precedence_example2 WHERE s1 = s2;