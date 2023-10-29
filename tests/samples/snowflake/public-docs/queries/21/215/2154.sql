-- see https://docs.snowflake.com/en/sql-reference/account-usage/tags

select * from snowflake.account_usage.tags
order by tag_name;