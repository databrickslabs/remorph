-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select id, string1,
    regexp_substr(string1, 'A\\W+(\\w+)', 1, 1,    'e', 1) as "SUBSTRING1",
    regexp_instr( string1, 'A\\W+(\\w+)', 1, 1, 0, 'e', 1) as "POSITION1",
    regexp_substr(string1, 'A\\W+(\\w+)', 1, 2,    'e', 1) as "SUBSTRING2",
    regexp_instr( string1, 'A\\W+(\\w+)', 1, 2, 0, 'e', 1) as "POSITION2",
    regexp_substr(string1, 'A\\W+(\\w+)', 1, 3,    'e', 1) as "SUBSTRING3",
    regexp_instr( string1, 'A\\W+(\\w+)', 1, 3, 0, 'e', 1) as "POSITION3",
    regexp_substr(string1, 'A\\W+(\\w+)', 1, 4,    'e', 1) as "SUBSTRING4",
    regexp_instr( string1, 'A\\W+(\\w+)', 1, 4, 0, 'e', 1) as "POSITION4"
    from demo3;