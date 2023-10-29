-- see https://docs.snowflake.com/en/sql-reference/sql/create-clone

CREATE TABLE orders_clone_restore CLONE orders BEFORE (STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');