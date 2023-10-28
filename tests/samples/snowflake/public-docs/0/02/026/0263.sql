SET QUERY_10 = 'SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID';
CREATE TABLE json_explain_output_for_analysis (
    ID INTEGER,
    query VARCHAR,
    explain_plan VARCHAR
    );
INSERT INTO json_explain_output_for_analysis (ID, query, explain_plan) 
    SELECT 
        1,
        $QUERY_10 AS query,
        SYSTEM$EXPLAIN_PLAN_JSON($QUERY_10) AS explain_plan;