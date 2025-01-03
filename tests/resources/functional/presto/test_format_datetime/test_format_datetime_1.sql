-- presto sql:
select
  format_datetime(current_timestamp,'EEEE') as col1
, format_datetime(current_date,'EEEE') as col2
, format_datetime(from_unixtime(1732723200), 'hh:mm:ss a') as col3
, format_datetime(from_unixtime(1732723200), 'yyyy-MM-dd HH:mm:ss EEEE') as col4;

-- databricks sql:
SELECT
  DATE_FORMAT(CURRENT_TIMESTAMP(), 'EEEE') AS col1,
  DATE_FORMAT(CURRENT_DATE(), 'EEEE') AS col2,
  DATE_FORMAT(CAST(FROM_UNIXTIME(1732723200) AS TIMESTAMP), 'hh:mm:ss a') AS col3,
  DATE_FORMAT(CAST(FROM_UNIXTIME(1732723200) AS TIMESTAMP), 'yyyy-MM-dd HH:mm:ss EEEE') AS col4
