-- see https://docs.snowflake.com/en/sql-reference/data-sharing-usage/listing-access-history

select
  los.value:"objectDomain"::string as object_type,
  los.value:"objectName"::string as object_name,
  cols.value:"columnName"::string as column_name,
  count(distinct lah.query_token) as n_queries,
  count(distinct lah.consumer_account_locator) as n_distinct_consumer_accounts
from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
join lateral flatten(input=>lah.listing_objects_accessed) as los
join lateral flatten(input=>los.value, path=>'columns') as cols
where true
  and los.value:"objectDomain"::string in ('Table', 'View')
  and query_date between '2022-03-01' and '2022-04-30'
  and los.value:"objectName"::string = 'DATABASE_NAME.SCHEMA_NAME.TABLE_NAME'
  and lah.consumer_account_locator = 'CONSUMER_ACCOUNT_LOCATOR'
group by 1,2,3;