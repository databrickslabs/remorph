select id, string1, 
    regexp_substr(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1,    'e', 1) as "SUBSTR1",
    regexp_instr( string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 0, 'e', 1) as "POS1",
    regexp_substr(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1,    'e', 2) as "SUBSTR2",
    regexp_instr( string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 0, 'e', 2) as "POS2",
    regexp_substr(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1,    'e', 3) as "SUBSTR3",
    regexp_instr( string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 0, 'e', 3) as "POS3"
    from demo3;