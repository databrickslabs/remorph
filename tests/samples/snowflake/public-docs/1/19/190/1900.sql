SELECT value:phaseName::string AS "Phase",
  value:resultName::string AS "Result",
  TO_TIMESTAMP_LTZ(value:startTimeUTC::numeric,3) AS "startTime",
  TO_TIMESTAMP_LTZ(value:endTimeUTC::numeric,3) AS "endTime",
  value:details AS "details"
  FROM table(flatten(INPUT=> PARSE_JSON(SYSTEM$DATABASE_REFRESH_PROGRESS('mydb1'))));