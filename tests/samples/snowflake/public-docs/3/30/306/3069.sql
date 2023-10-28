CALL budget_db.budget_schema.my_budget!ADD_RESOURCE(
  SELECT SYSTEM$REFERENCE('TABLE', 't2', 'SESSION', 'APPLYBUDGET'));