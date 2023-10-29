-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_replace

select regexp_replace('firstname middlename lastname','(.*) (.*) (.*)','\\3, \\1 \\2') as "name sort" from dual;
