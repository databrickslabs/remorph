-- see https://docs.snowflake.com/en/sql-reference/functions/collate

SELECT spanish_phrase FROM collation_demo 
  ORDER BY spanish_phrase COLLATE 'utf8';