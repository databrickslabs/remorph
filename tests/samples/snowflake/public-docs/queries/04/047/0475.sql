-- see https://docs.snowflake.com/en/sql-reference/constructs/from

CREATE TABLE ftable1 (retail_price FLOAT, wholesale_cost FLOAT, description VARCHAR);
INSERT INTO ftable1 (retail_price, wholesale_cost, description) 
  VALUES (14.00, 6.00, 'bling');