-- see https://docs.snowflake.com/en/sql-reference/sql/create-external-table

CREATE EXTERNAL TABLE ext_twitter_feed(
 date_part date AS TO_DATE(SPLIT_PART(metadata$filename, '/', 3)
   || '/' || SPLIT_PART(metadata$filename, '/', 4)
   || '/' || SPLIT_PART(metadata$filename, '/', 5), 'YYYY/MM/DD'),
 timestamp bigint AS (value:timestamp::bigint),
 col2 varchar AS (value:col2::varchar))
 PARTITION BY (date_part)
 LOCATION=@mystage/daily/
 REFRESH_ON_CREATE =  FALSE
 AUTO_REFRESH = FALSE
 FILE_FORMAT = (TYPE = PARQUET)
 TABLE_FORMAT = DELTA;