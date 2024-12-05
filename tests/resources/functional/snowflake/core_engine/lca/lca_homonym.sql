-- snowflake sql:
select
  ca_zip
from (
  SELECT
    substr(ca_zip,1,5) ca_zip,
    trim(name) as name,
    count(*) over( partition by ca_zip)
  FROM
    customer_address
  WHERE
    ca_zip IN ('89436', '30868'));
-- databricks sql:
SELECT
  ca_zip
FROM
SELECT
  SUBSTR(ca_zip,1,5) AS ca_zip,
  TRIM(name) AS name,
  COUNT(*) OVER (
    PARTITION BY
      SUBSTR(ca_zip,1,5)
  )
FROM
  customer_address
WHERE
  SUBSTR(ca_zip,1,5) IN ('89436', '30868');
