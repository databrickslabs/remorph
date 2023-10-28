CREATE OR REPLACE TABLE collation_precedence_example(
  col1    VARCHAR,               -- equivalent to COLLATE ''
  col2_fr VARCHAR COLLATE 'fr',  -- French locale
  col3_de VARCHAR COLLATE 'de'   -- German locale
);