select query_type,
       warehouse_size,
       avg(execution_time) as average_execution_time
from query_history
where start_time >= date_trunc(month, current_date)
group by 1,2
order by 3 desc;