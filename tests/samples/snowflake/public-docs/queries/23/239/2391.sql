-- see https://docs.snowflake.com/en/sql-reference/account-usage

select user_name,
       count(*) as failed_logins,
       avg(seconds_between_login_attempts) as average_seconds_between_login_attempts
from (
      select user_name,
             timediff(seconds, event_timestamp, lead(event_timestamp)
                 over(partition by user_name order by event_timestamp)) as seconds_between_login_attempts
      from login_history
      where event_timestamp > date_trunc(month, current_date)
      and is_success = 'NO'
     )
group by 1
order by 3;