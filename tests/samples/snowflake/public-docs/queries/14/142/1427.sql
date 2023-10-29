-- see https://docs.snowflake.com/en/sql-reference/functions/system_explain_json_to_text

SELECT SYSTEM$EXPLAIN_JSON_TO_TEXT(explain_plan) 
    FROM json_explain_output_for_analysis
    WHERE json_explain_output_for_analysis.ID = 1;