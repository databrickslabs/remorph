-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

INSERT INTO array_example (array_column)
    SELECT [ 12, 'twelve', NULL ];