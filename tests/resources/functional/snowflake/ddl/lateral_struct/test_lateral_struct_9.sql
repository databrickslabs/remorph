-- snowflake sql:
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

-- databricks sql:
SELECT
  CAST(los.objectDomain AS STRING) AS object_type,
  CAST(los.objectName AS STRING) AS object_name,
  CAST(cols.columnName AS STRING) AS column_name,
  COUNT(DISTINCT lah.query_token) AS n_queries,
  COUNT(DISTINCT lah.consumer_account_locator) AS n_distinct_consumer_accounts
FROM SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY AS lah
LATERAL VIEW EXPLODE(lah.listing_objects_accessed) AS los
LATERAL VIEW EXPLODE(los.value.columns) AS cols
WHERE true AND CAST(los.value.objectDomain AS STRING) IN ('Table', 'View') AND
query_date BETWEEN '2022-03-01' AND '2022-04-30' AND
CAST(los.value.objectName AS STRING) = 'DATABASE_NAME.SCHEMA_NAME.TABLE_NAME' AND
lah.consumer_account_locator = 'CONSUMER_ACCOUNT_LOCATOR' GROUP BY 1, 2, 3;
