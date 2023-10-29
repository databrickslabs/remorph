-- see https://docs.snowflake.com/en/sql-reference/data-types-text

CREATE OR REPLACE TABLE test_binary(b BINARY,
                                    b100 BINARY(100),
                                    vb VARBINARY
                                    );

DESC TABLE test_binary;
