-- see https://docs.snowflake.com/en/sql-reference/functions/explain_json

SELECT * FROM TABLE(
    EXPLAIN_JSON(
        SYSTEM$EXPLAIN_PLAN_JSON(
           'SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID')
        )
    );