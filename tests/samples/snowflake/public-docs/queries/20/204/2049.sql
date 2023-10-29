-- see https://docs.snowflake.com/en/sql-reference/functions/policy_context

execute using policy_context(current_role => 'PUBLIC') as select * from empl_info;