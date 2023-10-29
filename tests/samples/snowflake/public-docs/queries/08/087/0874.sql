-- see https://docs.snowflake.com/en/sql-reference/functions/flatten

SELECT * FROM TABLE(FLATTEN(input => parse_json('{"a":1, "b":[77,88], "c": {"d":"X"}}'),
                            recursive => true, mode => 'object' )) f;
