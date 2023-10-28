select id, string1,
      regexp_substr(string1, 'nevermore\\d') AS "SUBSTRING", 
      regexp_instr( string1, 'nevermore\\d') AS "POSITION"
    from demo1
    order by id;