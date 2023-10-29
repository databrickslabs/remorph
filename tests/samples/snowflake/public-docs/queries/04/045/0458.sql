-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

CREATE TABLE demo2 (id INT, string1 VARCHAR);
INSERT INTO demo2 (id, string1) VALUES 
    -- A string with multiple occurrences of the word "the".
    (2, 'It was the best of times, it was the worst of times.'),
    -- A string with multiple occurrences of the word "the" and with extra
    -- blanks between words.
    (3, 'In    the   string   the   extra   spaces  are   redundant.'),
    -- A string with the character sequence "the" inside multiple words 
    -- ("thespian" and "theater"), but without the word "the" by itself.
    (4, 'A thespian theater is nearby.')
    ;