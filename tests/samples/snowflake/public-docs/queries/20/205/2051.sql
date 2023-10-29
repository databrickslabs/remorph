-- see https://docs.snowflake.com/en/sql-reference/account-usage/access_history

insert into a(c1)
select c2
from b
where c3 > 1;