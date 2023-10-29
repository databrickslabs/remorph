-- see https://docs.snowflake.com/en/sql-reference/functions/invoker_share

create or replace masking policy mask_share
as (val string) returns string ->
case
  when invoker_share() in ('SHARE1') then mask1_function(val)
  when invoker_share() in ('SHARE2') then mask2_function(val)
  else '***MASKED***'
end;