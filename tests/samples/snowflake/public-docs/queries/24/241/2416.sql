-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_authorized_endpoints

use role accountadmin;
select system$get_privatelink_authorized_endpoints();