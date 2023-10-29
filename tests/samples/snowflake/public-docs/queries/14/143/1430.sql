-- see https://docs.snowflake.com/en/sql-reference/functions/system_explain_plan_json

SELECT SYSTEM$EXPLAIN_PLAN_JSON(LAST_QUERY_ID()) AS explain_plan;