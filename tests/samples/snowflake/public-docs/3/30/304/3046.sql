CALL snowflake.local.account_root_budget!GET_SPENDING_HISTORY(
  TIME_LOWER_BOUND=>dateadd('days', -7, current_timestamp()),
  TIME_UPPER_BOUND=>current_timestamp()
);