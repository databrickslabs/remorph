-- see https://docs.snowflake.com/en/sql-reference/constraints-properties

ALTER TABLE table_with_primary_key ALTER CONSTRAINT a_primary_key_constraint RELY;
ALTER TABLE table_with_foreign_key ALTER CONSTRAINT a_foreign_key_constraint RELY;