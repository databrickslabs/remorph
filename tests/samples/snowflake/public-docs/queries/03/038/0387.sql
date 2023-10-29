-- see https://docs.snowflake.com/en/sql-reference/data-types-text

CREATE OR REPLACE TABLE test_text(v VARCHAR,
                                  v50 VARCHAR(50),
                                  c CHAR,
                                  c10 CHAR(10),
                                  s STRING,
                                  s20 STRING(20),
                                  t TEXT,
                                  t30 TEXT(30)
                                  );

DESC TABLE test_text;
