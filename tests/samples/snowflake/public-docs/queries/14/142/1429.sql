-- see https://docs.snowflake.com/en/sql-reference/functions/system_explain_plan_json

SELECT SYSTEM$EXPLAIN_PLAN_JSON(
    'SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID'
    ) AS explain_plan;