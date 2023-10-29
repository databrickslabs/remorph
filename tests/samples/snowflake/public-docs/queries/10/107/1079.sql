-- see https://docs.snowflake.com/en/sql-reference/functions/count

SELECT COUNT(v:Title)
    FROM count_example_with_variant_column;