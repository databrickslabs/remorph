-- see https://docs.snowflake.com/en/sql-reference/classes/budget/methods/set_email_notifications

CALL budget_db.budget_schema.my_budget!SET_EMAIL_NOTIFICATIONS(
   'budgets_notification', 'costadmin@domain.com, budgetadmin@domain.com');