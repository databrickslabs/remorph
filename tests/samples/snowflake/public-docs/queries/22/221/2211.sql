-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select body, regexp_instr(body, '\\b\\S*o\\S*\\b', 3, 3, 1, 'i') as result from message;
