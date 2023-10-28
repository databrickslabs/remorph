with
accesses as (
  select distinct
    los.value:"objectDomain"::string as object_type,
    los.value:"objectName"::string as object_name,
    lah.query_token,
    lah.consumer_account_locator
  from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
  join lateral flatten(input=>lah.listing_objects_accessed) as los
  where true
    and los.value:"objectDomain"::string in ('Table', 'View')
    and query_date between '2022-03-01' and '2022-04-30'
)
select
  a1.object_name as object_name_1,
  a2.object_name as object_name_2,
  a1.consumer_account_locator as consumer_account_locator,
  count(distinct a1.query_token) as n_queries
from accesses as a1
join accesses as a2
  on a1.query_token = a2.query_token
  and a1.object_name < a2.object_name
group by 1,2,3;