--Query type: DML
DECLARE @jsonData NVARCHAR(MAX) = N'{"data":{"values":[{"id":1,"name":"John"},{"id":2,"name":"Jane"}]}}';
WITH json_data AS (
    SELECT JSON_VALUE(@jsonData, '$.data.values[0].id') AS id,
           JSON_VALUE(@jsonData, '$.data.values[0].name') AS name
)
SELECT * FROM json_data;
