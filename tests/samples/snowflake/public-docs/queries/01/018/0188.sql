-- see https://docs.snowflake.com/en/sql-reference/sql/create-table-constraint

ALTER TABLE table1 
    ADD COLUMN col3 VARCHAR NOT NULL CONSTRAINT uniq_col3 UNIQUE NOT ENFORCED;