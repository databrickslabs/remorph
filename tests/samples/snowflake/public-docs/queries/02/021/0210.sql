-- see https://docs.snowflake.com/en/sql-reference/classes/budget/methods/add_resource

CALL budget_db.budget_schema.my_budget!ADD_RESOURCE(
  SELECT SYSTEM$REFERENCE('TABLE', 't2', 'SESSION', 'APPLYBUDGET'));