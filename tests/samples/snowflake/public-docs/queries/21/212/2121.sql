-- see https://docs.snowflake.com/en/sql-reference/functions/tag_references

select *
  from table(my_db.information_schema.tag_references('my_table.result', 'COLUMN'));