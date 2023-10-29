-- see https://docs.snowflake.com/en/sql-reference/data-types-numeric

CREATE OR REPLACE TABLE test_float(d DOUBLE,
                                   f FLOAT,
                                   dp DOUBLE PRECISION,
                                   r REAL
                                   );

DESC TABLE test_float;
