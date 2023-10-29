-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

INSERT INTO object_example (object_column)
    SELECT { 'thirteen': 13::VARIANT, 'zero': 0::VARIANT };