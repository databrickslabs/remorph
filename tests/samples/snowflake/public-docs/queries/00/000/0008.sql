-- see https://docs.snowflake.com/en/sql-reference/sql/create-clone

-- Create a schema to serve as the source for a cloned schema.
CREATE SCHEMA source;

-- Create a table.
CREATE TABLE mytable (col1 string, col2 string);

-- Create a view that references the table with a fully-qualified name.
CREATE VIEW myview AS SELECT col1 FROM source.mytable;

-- Retrieve the DDL for the source schema.
SELECT GET_DDL ('schema', 'source', true);


-- Clone the source schema.
CREATE SCHEMA source_clone CLONE source;

-- Retrieve the DDL for the clone of the source schema.
-- The clone of the view references the source table with the same fully-qualified name
-- as in the view in the source schema.
SELECT GET_DDL ('schema', 'source_clone', true);
