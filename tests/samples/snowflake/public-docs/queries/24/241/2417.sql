-- see https://docs.snowflake.com/en/sql-reference/functions/rest_event_history

use role accountadmin;
use database my_db;
use schema information_schema;
select *
  from table(rest_event_history(
      rest_service_type => 'scim',
      time_range_start => dateadd('minutes',-5,current_timestamp()),
      time_range_end => current_timestamp(),
      200))
  order by event_timestamp;