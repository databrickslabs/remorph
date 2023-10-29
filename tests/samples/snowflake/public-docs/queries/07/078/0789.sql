-- see https://docs.snowflake.com/en/sql-reference/data-types-text

SELECT $1, $2 FROM VALUES ('row1', $$a
                                      ' \ \t
                                      \x21 z $ $$);
