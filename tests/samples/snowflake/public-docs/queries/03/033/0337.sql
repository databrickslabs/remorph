-- see https://docs.snowflake.com/en/sql-reference/sql/create-table

CREATE OR REPLACE TABLE parquet_col (
  custKey NUMBER DEFAULT NULL,
  orderDate DATE DEFAULT NULL,
  orderStatus VARCHAR(100) DEFAULT NULL,
  price VARCHAR(255)
)
AS SELECT
  $1:o_custkey::number,
  $1:o_orderdate::date,
  $1:o_orderstatus::text,
  $1:o_totalprice::text
FROM @my_stage;


DESC TABLE parquet_col;
