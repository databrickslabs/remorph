-- snowflake sql:
SELECT
  los.value:"objectDomain"::STRING AS object_type,
  los.value:"objectName"::STRING AS object_name,
  cols.value:"columnName"::STRING AS column_name,
  COUNT(DISTINCT lah:"query_token"::STRING) AS n_queries,
  COUNT(DISTINCT lah:"consumer_account_locator"::STRING) AS n_distinct_consumer_accounts
FROM
  (SELECT
    PARSE_JSON('{"query_date": "2022-03-02","query_token": "some_token","consumer_account_locator": "CONSUMER_ACCOUNT_LOCATOR","listing_objects_accessed": [{"objectDomain": "Table","objectName": "DATABASE_NAME.SCHEMA_NAME.TABLE_NAME","columns": [{"columnName": "column1"},{"columnName": "column2"}]}]}') AS lah
  ) AS src,
  LATERAL FLATTEN(input => src.lah:"listing_objects_accessed") AS los,
  LATERAL FLATTEN(input => los.value:"columns") AS cols
WHERE
  los.value:"objectDomain"::STRING IN ('Table', 'View') AND
  src.lah:"query_date"::DATE BETWEEN '2022-03-01' AND '2022-04-30' AND
  los.value:"objectName"::STRING = 'DATABASE_NAME.SCHEMA_NAME.TABLE_NAME' AND
  src.lah:"consumer_account_locator"::STRING = 'CONSUMER_ACCOUNT_LOCATOR'
GROUP BY 1, 2, 3;

-- databricks sql:
SELECT
  CAST (los:objectdomain as string) as object_type,
  CAST (los:objectname as string) as object_name,
  CAST (cols:columnname as string) as column_name,
  COUNT (DISTINCT CAST (lah:query_token as string)) as n_queries,
  COUNT (
    DISTINCT CAST (lah:consumer_account_locator as string)
  ) as n_distinct_consumer_accounts
FROM
  (
    SELECT
      parse_json (
        '{"query_date": "2022-03-02","query_token": "some_token","consumer_account_locator": "consumer_account_locator","listing_objects_accessed": [{"objectdomain": "table","objectname": "database_name.schema_name.table_name","columns": [{"columnname": "column1"},{"columnname": "column2"}]}]}'
      ) AS lah
  ) AS src
  LATERAL VIEW EXPLODE (CAST (src.lah:listing_objects_accessed AS ARRAY<VARIANT>)) AS los
  LATERAL VIEW EXPLODE (CAST (los:columns AS ARRAY<VARIANT>)) AS cols
WHERE
  CAST (los:objectdomain AS string) in ('table', 'view')
  AND CAST (src.lah:query_date AS DATE) BETWEEN '2022-03-01' AND '2022-04-30'
  AND CAST (los:objectname AS string) = 'database_name.schema_name.table_name'
  AND CAST (src.lah:consumer_account_locator AS string) = 'consumer_account_locator'
GROUP BY 1, 2, 3;