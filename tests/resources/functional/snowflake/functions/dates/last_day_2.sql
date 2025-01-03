-- snowflake sql:
select
  last_day(current_date()) as col,
  last_day(current_date(), 'YEAR') as col1,
  last_day(current_date(), 'QUARTER') as col2,
  last_day(current_date(), 'MONTH') as col3,
  last_day(current_date(), 'WEEK') as col4,
  last_day(current_timestamp()) as col5,
  last_day(current_timestamp(), 'YEAR') as col6,
  last_day(current_timestamp(), 'QUARTER') as col7,
  last_day(current_timestamp(), 'MONTH') as col8,
  last_day(current_timestamp(), 'WEEK') as col9,
  last_day(date('2021-01-01')) as col10,
  last_day(date('2021-01-01'), 'YEAR') as col11,
  last_day(date('2021-01-01'), 'QUARTER') as col12,
  last_day(date('2021-01-01'), 'MONTH') as col13,
  last_day(date('2021-01-01'), 'WEEK') as col14;

-- databricks sql:
SELECT
  LAST_DAY(CURRENT_DATE()) AS col,
  DATE_ADD(DATEADD(YEAR, 1, TRUNC(CURRENT_DATE(), 'YEAR')), -1) AS col1,
  DATE_ADD(DATEADD(QUARTER, 1, TRUNC(CURRENT_DATE(), 'QUARTER')), -1) AS col2,
  DATE_ADD(DATEADD(MONTH, 1, TRUNC(CURRENT_DATE(), 'MONTH')), -1) AS col3,
  DATE_ADD(DATEADD(WEEK, 1, TRUNC(CURRENT_DATE(), 'WEEK')), -1) AS col4,
  LAST_DAY(CURRENT_TIMESTAMP()) AS col5,
  DATE_ADD(DATEADD(YEAR, 1, TRUNC(CURRENT_TIMESTAMP(), 'YEAR')), -1) AS col6,
  DATE_ADD(DATEADD(QUARTER, 1, TRUNC(CURRENT_TIMESTAMP(), 'QUARTER')), -1) AS col7,
  DATE_ADD(DATEADD(MONTH, 1, TRUNC(CURRENT_TIMESTAMP(), 'MONTH')), -1) AS col8,
  DATE_ADD(DATEADD(WEEK, 1, TRUNC(CURRENT_TIMESTAMP(), 'WEEK')), -1) AS col9,
  LAST_DAY(CAST('2021-01-01' AS DATE)) AS col10,
  DATE_ADD(DATEADD(YEAR, 1, TRUNC(CAST('2021-01-01' AS DATE), 'YEAR')), -1) AS col11,
  DATE_ADD(DATEADD(QUARTER, 1, TRUNC(CAST('2021-01-01' AS DATE), 'QUARTER')), -1) AS col12,
  DATE_ADD(DATEADD(MONTH, 1, TRUNC(CAST('2021-01-01' AS DATE), 'MONTH')), -1) AS col13,
  DATE_ADD(DATEADD(WEEK, 1, TRUNC(CAST('2021-01-01' AS DATE), 'WEEK')), -1) AS col14;
