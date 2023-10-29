-- see https://docs.snowflake.com/en/sql-reference/collation

SELECT * FROM collation_demo WHERE spanish_phrase = uncollated_phrase;