-- see https://docs.snowflake.com/en/sql-reference/sql/delete

CREATE TABLE leased_bicycles (bicycle_id INTEGER, customer_id INTEGER);
CREATE TABLE returned_bicycles (bicycle_id INTEGER);