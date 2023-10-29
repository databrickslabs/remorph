-- see https://docs.snowflake.com/en/sql-reference/functions/ltrim

SELECT '>' || v || '<' AS Original,
       '>' || LTRIM(v, (SELECT whitespace_char FROM c_compatible_whitespace)) || '<' AS LTrimmed
    FROM t1;