--Query type: DQL
DECLARE @json nvarchar(max) = (SELECT History FROM DatabaseRefreshHistory WHERE DatabaseName = 'mydb');
WITH temp_result AS (
  SELECT 
    start_time = JSON_VALUE(value, '$.startTimeUTC'),
    end_time = JSON_VALUE(value, '$.endTimeUTC'),
    phase = JSON_VALUE(value, '$.currentPhase'),
    query_ID = JSON_VALUE(value, '$.jobUUID'),
    bytes_transferred = JSON_VALUE(value, '$.copy_bytes')
  FROM 
    OPENJSON(@json)
  WITH (
    value nvarchar(max) '$' AS JSON
  )
)
SELECT 
  start_time,
  end_time,
  phase,
  query_ID,
  bytes_transferred
FROM 
  temp_result;