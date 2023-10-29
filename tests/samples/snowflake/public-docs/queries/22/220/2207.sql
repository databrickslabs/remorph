-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_instr

select body, regexp_instr(body, '\\b\\S*o\\S*\\b') as result from message;
