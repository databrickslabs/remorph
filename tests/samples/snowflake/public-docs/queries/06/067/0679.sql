-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

INSERT INTO object_example (object_column)
    SELECT OBJECT_CONSTRUCT('thirteen', 13::VARIANT, 'zero', 0::VARIANT);