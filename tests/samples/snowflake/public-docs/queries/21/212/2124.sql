-- see https://docs.snowflake.com/en/sql-reference/functions/tag_references_with_lineage

select *
  from table(snowflake.account_usage.tag_references_with_lineage('my_db.my_schema.cost_center'));