--Query type: DML
DECLARE @msg NVARCHAR(2048) = FORMATMESSAGE(60000, 500, N'First string', N'second string');
WITH temp_result AS (
    SELECT 'First string' AS string1, 'Second string' AS string2
)
SELECT 
    string1, 
    string2, 
    @msg AS message
FROM 
    temp_result;
THROW 60000, @msg, 1;