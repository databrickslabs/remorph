SELECT value:phaseName::string AS "Phase",
  value:resultName::string AS "Result",
  TO_TIMESTAMP_LTZ(value:startTimeUTC::numeric,3) AS "startTime",
  TO_TIMESTAMP_LTZ(value:endTimeUTC::numeric,3) AS "endTime",
  value:details AS "details"
  FROM TABLE(FLATTEN(input=> PARSE_JSON(SYSTEM$DATABASE_REFRESH_PROGRESS_BY_JOB('4cbd7187-51f6-446c-9814-92d7f57d939b'))));