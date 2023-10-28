SELECT
    to_timestamp_ltz(value:startTimeUTC::numeric,3) AS "start_time"
    , to_timestamp_ltz(value:endTimeUTC::numeric,3) AS "end_time"
    , value:currentPhase::string AS "phase"
  , value:jobUUID::string AS "query_ID"
  , value:copy_bytes::integer AS "bytes_transferred"
FROM TABLE(flatten(INPUT=> PARSE_JSON(SYSTEM$DATABASE_REFRESH_HISTORY('mydb'))));