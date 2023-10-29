-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select id, string1,
      regexp_substr(string1, 'nevermore\\d', 5) AS "SUBSTRING", 
      regexp_instr( string1, 'nevermore\\d', 5) AS "POSITION"
    from demo1
    order by id;