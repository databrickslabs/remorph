-- see https://docs.snowflake.com/en/sql-reference/account-usage/row_access_policies

select policy_name, policy_signature, created
from row_access_policies
order by created
;