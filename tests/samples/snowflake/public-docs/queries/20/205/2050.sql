-- see https://docs.snowflake.com/en/sql-reference/account-usage/access_history

insert into A(col1) select f(col2) from B;