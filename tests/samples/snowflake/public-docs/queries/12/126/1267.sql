-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

SELECT OBJECT_CONSTRUCT(
    'name', 'Jones'::VARIANT,
    'age',  42::VARIANT
    );