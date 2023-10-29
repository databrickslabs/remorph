-- see https://docs.snowflake.com/en/sql-reference/account-usage

USE ROLE ACCOUNTADMIN;

GRANT IMPORTED PRIVILEGES ON DATABASE snowflake TO ROLE SYSADMIN;
GRANT IMPORTED PRIVILEGES ON DATABASE snowflake TO ROLE customrole1;

USE ROLE customrole1;

SELECT database_name, database_owner FROM snowflake.account_usage.databases;