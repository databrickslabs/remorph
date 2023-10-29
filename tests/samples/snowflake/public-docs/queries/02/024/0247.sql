-- see https://docs.snowflake.com/en/sql-reference/classes/budget/methods/set_email_notifications

CALL snowflake.local.account_root_budget!SET_EMAIL_NOTIFICATIONS(
   'budgets_notification', 'budgetadmin@domain.com');