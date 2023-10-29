-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select id, string1,
       regexp_substr(string1, 'the\\W+(\\w+)', 1, 2,    '', 1) as "SUBSTRING",
       regexp_instr( string1, 'the\\W+(\\w+)', 1, 2, 0, '', 1) as "POSITION"
    from demo2
    order by id;