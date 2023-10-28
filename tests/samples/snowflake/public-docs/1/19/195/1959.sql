use role accountadmin;

select SYSTEM$REVOKE_STAGE_PRIVATELINK_ACCESS('/subscriptions/subId/resourceGroups/rg1/providers/Microsoft.Network/privateEndpoints/pe1');