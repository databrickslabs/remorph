use role accountadmin;

select SYSTEM$AUTHORIZE_PRIVATELINK(
  '/subscriptions/26d.../resourcegroups/sf-1/providers/microsoft.network/privateendpoints/test-self-service',
  'eyJ...');