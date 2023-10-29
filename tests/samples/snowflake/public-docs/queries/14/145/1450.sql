-- see https://docs.snowflake.com/en/sql-reference/classes/budget/methods/add_resource

SELECT SYSTEM$REFERENCE('TABLE', 't1', 'SESSION', 'APPLYBUDGET');