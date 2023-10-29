-- see https://docs.snowflake.com/en/sql-reference/functions/system_authorize_stage_privatelink_access

use role accountadmin;

select SYSTEM$AUTHORIZE_STAGE_PRIVATELINK_ACCESS('/subscriptions/subId/resourceGroups/rg1/providers/Microsoft.Network/privateEndpoints/pe1');