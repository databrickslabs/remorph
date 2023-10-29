-- see https://docs.snowflake.com/en/sql-reference/classes/budget/methods/set_notification_mute_flag

CALL snowflake.local.account_root_budget!SET_NOTIFICATION_MUTE_FLAG(FALSE);