select id, name FROM tracker_1
union all
select id, name FROM tracker_2
order by id;