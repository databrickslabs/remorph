-- see https://docs.snowflake.com/en/sql-reference/classes/budget/methods/set_spending_limit

CALL snowflake.local.account_root_budget!SET_SPENDING_LIMIT(500);