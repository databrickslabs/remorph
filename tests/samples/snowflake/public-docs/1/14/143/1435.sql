select * from table(information_schema.notification_history(
  START_TIME=>dateadd('hour',-1,current_timestamp()),
  END_TIME=>current_timestamp(),
  RESULT_LIMIT=>100,
  INTEGRATION_NAME=>'MY_INTEGRATION'));