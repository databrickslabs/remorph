-- see https://docs.snowflake.com/en/sql-reference/functions/system_revoke_stage_privatelink_access

use role accountadmin;

select SYSTEM$REVOKE_STAGE_PRIVATELINK_ACCESS('/subscriptions/subId/resourceGroups/rg1/providers/Microsoft.Network/privateEndpoints/pe1');