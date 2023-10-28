select reported_client_type,
       user_name,
       sum(iff(is_success = 'NO', 1, 0)) as failed_logins,
       count(*) as logins,
       sum(iff(is_success = 'NO', 1, 0)) / nullif(count(*), 0) as login_failure_rate
from login_history
where event_timestamp > date_trunc(month, current_date)
group by 1,2
order by 5 desc;