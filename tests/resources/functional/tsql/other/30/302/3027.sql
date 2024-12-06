-- tsql sql:
DECLARE @position INT, @string CHAR(8);
SET @position = 1;
SET @string = 'New Moon';

WHILE @position <= DATALENGTH(@string)
BEGIN
    SELECT ASCII(SUBSTRING(@string, @position, 1)) AS ascii_value,
           CHAR(ASCII(SUBSTRING(@string, @position, 1))) AS char_value;
    SET @position = @position + 1;
END;
