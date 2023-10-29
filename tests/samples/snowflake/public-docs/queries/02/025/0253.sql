-- see https://docs.snowflake.com/en/sql-reference/sql/comment

COMMENT [IF EXISTS] ON <object_type> <object_name> IS '<string_literal>';

COMMENT [IF EXISTS] ON COLUMN <table_name>.<column_name> IS '<string_literal>';