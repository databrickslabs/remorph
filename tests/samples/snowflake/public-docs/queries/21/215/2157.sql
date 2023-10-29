-- see https://docs.snowflake.com/en/sql-reference/functions/startswith

select * from strings;


select * from strings where startswith(s, 'te');
