-- see https://docs.snowflake.com/en/sql-reference/collation

SELECT spanish_phrase FROM collation_demo 
  ORDER BY COLLATE(spanish_phrase, 'utf8');