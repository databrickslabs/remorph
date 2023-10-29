-- see https://docs.snowflake.com/en/sql-reference/functions/system_explain_json_to_text

SELECT query, explain_plan FROM json_explain_output_for_analysis;