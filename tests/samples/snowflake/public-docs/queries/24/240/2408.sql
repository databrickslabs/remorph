-- see https://docs.snowflake.com/en/sql-reference/functions/get_query_operator_stats

set lqid = (select last_query_id());