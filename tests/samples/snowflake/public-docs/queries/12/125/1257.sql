-- see https://docs.snowflake.com/en/sql-reference/account-usage/class_instances

SELECT NAME, DATABASE_NAME, SCHEMA_NAME, CLASS_NAME
  FROM SNOWFLAKE.ACCOUNT_USAGE.CLASS_INSTANCES
  WHERE CLASS_NAME = 'ANOMALY_DETECTION';