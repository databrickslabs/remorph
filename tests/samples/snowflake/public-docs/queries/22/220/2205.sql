-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select body, regexp_instr(body, '\\S*(o)\\S*\\b', 1, 1, 0, 'i') as result from message;
