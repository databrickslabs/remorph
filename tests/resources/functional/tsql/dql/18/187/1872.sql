--Query type: DQL
DECLARE @date DATE = '1995-12-13';
DECLARE @datetimeoffset DATETIMEOFFSET(4) = '1995-12-13 00:00:00+00:00';
SELECT *
FROM (
    VALUES (@date, @datetimeoffset)
) AS temp_result ([date], [datetimeoffset(4)]);
