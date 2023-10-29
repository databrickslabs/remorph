-- see https://docs.snowflake.com/en/sql-reference/functions/validate

CREATE OR REPLACE TABLE save_copy_errors AS SELECT * FROM TABLE(VALIDATE(t1, JOB_ID=>'5415fa1e-59c9-4dda-b652-533de02fdcf1'));