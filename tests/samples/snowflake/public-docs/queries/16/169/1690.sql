-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

SELECT object_column['thirteen'],
       object_column:thirteen
    FROM object_example;