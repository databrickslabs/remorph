-- see https://docs.snowflake.com/en/sql-reference/functions/count

SELECT i_col, j_col, v, v:Title
    FROM count_example_with_variant_column
    ORDER BY i_col;