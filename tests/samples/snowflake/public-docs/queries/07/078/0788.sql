-- see https://docs.snowflake.com/en/sql-reference/data-types-text

SELECT $1, $2 FROM
VALUES
('Tab','Hello\tWorld'),
('Newline','Hello\nWorld'),
('Backslash','C:\\user'),
('Octal','-\041-'),
('Hexadecimal','-\x21-'),
('Unicode','-\u26c4-'),
('Not an escape sequence', '\z')
;
