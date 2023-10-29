-- see https://docs.snowflake.com/en/sql-reference/constructs/group-by-grouping-sets

SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY GROUPING SETS (medical_license, radio_license);