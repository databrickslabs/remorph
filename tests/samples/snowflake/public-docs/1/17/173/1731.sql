select id, string1, 
       regexp_substr(string1, 'nevermore', 1, 4) AS "SUBSTRING",
       regexp_instr( string1, 'nevermore', 1, 4) AS "POSITION"
    from demo1
    order by id;