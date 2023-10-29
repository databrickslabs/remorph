-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_authorized_endpoints

select
  value: endpointId
from
  table(
    flatten(
      input => parse_json(system$get_privatelink_authorized_endpoints())
    )
  );