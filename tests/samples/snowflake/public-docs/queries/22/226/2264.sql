-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select id, string1,
      regexp_substr(string1, 'nevermore\\d', 1, 3) AS "SUBSTRING", 
      regexp_instr( string1, 'nevermore\\d', 1, 3) AS "POSITION"
    from demo1
    order by id;