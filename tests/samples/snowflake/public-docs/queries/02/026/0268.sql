-- see https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table

CREATE OR REPLACE DYNAMIC TABLE product
 TARGET_LAG = '20 minutes'
  WAREHOUSE = mywh
  AS
    SELECT product_id, product_name FROM staging_table;