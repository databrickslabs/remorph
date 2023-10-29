-- see https://docs.snowflake.com/en/sql-reference/functions/policy_references

use database my_db;
use schema information_schema;
select *
  from table(information_schema.policy_references(ref_entity_name => 'my_db.my_schema.my_table', ref_entity_domain => 'table'));