select a.PIPE_CATALOG as PIPE_CATALOG,
       a.PIPE_SCHEMA as PIPE_SCHEMA,
       a.PIPE_NAME as PIPE_NAME,
       b.CREDITS_USED as CREDITS_USED
from PIPES a join PIPE_USAGE_HISTORY b
on a.pipe_id = b.pipe_id
where b.START_TIME > date_trunc(month, current_date);