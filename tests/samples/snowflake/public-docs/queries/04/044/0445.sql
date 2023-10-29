-- see https://docs.snowflake.com/en/sql-reference/collation

CREATE TABLE collation_demo (
  uncollated_phrase VARCHAR, 
  utf8_phrase VARCHAR COLLATE 'utf8',
  english_phrase VARCHAR COLLATE 'en',
  spanish_phrase VARCHAR COLLATE 'sp'
  );

INSERT INTO collation_demo (uncollated_phrase, utf8_phrase, english_phrase, spanish_phrase) 
   VALUES ('pinata', 'pinata', 'pinata', 'piñata');