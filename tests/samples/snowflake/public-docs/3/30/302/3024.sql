CALL snowflake.local.account_root_budget!GET_SERVICE_TYPE_USAGE(
   SERVICE_TYPE => 'WAREHOUSE_METERING',
   TIME_DEPART => 'day',
   USER_TIMEZONE => 'UTC',
   TIME_LOWER_BOUND => dateadd('day', -7, current_timestamp()),
   TIME_UPPER_BOUND => current_timestamp()
);