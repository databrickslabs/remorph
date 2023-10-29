-- see https://docs.snowflake.com/en/sql-reference/classes/budget/methods/get_spending_limit

CALL snowflake.local.account_root_budget!GET_SPENDING_LIMIT();