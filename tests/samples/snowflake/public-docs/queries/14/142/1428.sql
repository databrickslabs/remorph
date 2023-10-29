-- see https://docs.snowflake.com/en/sql-reference/functions/system_explain_plan_json

SELECT SYSTEM$EXPLAIN_PLAN_JSON(
    $$ SELECT symptom, IFNULL(diagnosis, '(not yet diagnosed)') FROM medical $$
    );