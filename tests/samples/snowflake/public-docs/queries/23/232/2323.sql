-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr_all

select regexp_substr_all('a1_a2a3_a4A5a6', '(a)([[:digit:]])', 1, 1, 'ie') as matches;