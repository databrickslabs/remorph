-- see https://docs.snowflake.com/en/sql-reference/transactions

select id, name from tracker_1
union all
select id, name from tracker_2
union all
select id, name from tracker_3
order by id;