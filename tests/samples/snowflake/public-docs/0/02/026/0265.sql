SELECT SYSTEM$EXPLAIN_JSON_TO_TEXT(explain_plan) 
    FROM json_explain_output_for_analysis
    WHERE json_explain_output_for_analysis.ID = 1;