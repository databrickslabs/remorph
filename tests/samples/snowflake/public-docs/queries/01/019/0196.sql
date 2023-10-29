-- see https://docs.snowflake.com/en/sql-reference/functions/count

BEGIN WORK;

-- SQL NULL for both a VARIANT column and a non-VARIANT column.
INSERT INTO count_example_with_variant_column (i_col, j_col, v) VALUES (NULL, 10, NULL);
-- VARIANT NULL (aka JSON null)
INSERT INTO count_example_with_variant_column (i_col, j_col, v) SELECT 1, 11, PARSE_JSON('{"Title": null}');
-- VARIANT NON-NULL
INSERT INTO count_example_with_variant_column (i_col, j_col, v) SELECT 2, 12, PARSE_JSON('{"Title": "O"}');
INSERT INTO count_example_with_variant_column (i_col, j_col, v) SELECT 3, 12, PARSE_JSON('{"Title": "I"}');

COMMIT WORK;