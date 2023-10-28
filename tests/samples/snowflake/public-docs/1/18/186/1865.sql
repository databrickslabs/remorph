use role accountadmin;

select SYSTEM$GET_PRIVATELINK(
  '/subscriptions/26d.../resourcegroups/sf-1/providers/microsoft.network/privateendpoints/test-self-service',
  'eyJ...');