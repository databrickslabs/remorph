-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

CREATE OR REPLACE TABLE test_semi_structured(var VARIANT,
                                    arr ARRAY,
                                    obj OBJECT
                                    );

DESC TABLE test_semi_structured;
