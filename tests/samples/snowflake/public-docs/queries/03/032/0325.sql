-- see https://docs.snowflake.com/en/sql-reference/functions/ilike

CREATE OR REPLACE TABLE ilike_ex(subject varchar(20));
INSERT INTO ilike_ex VALUES
      ('John  Dddoe'),
      ('Joe   Doe'),
      ('John_down'),
      ('Joe down'),
      (null);