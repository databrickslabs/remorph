-- see https://docs.snowflake.com/en/sql-reference/functions/stage_directory_file_registration_history

SELECT *
  FROM TABLE(information_schema.stage_directory_file_registration_history(
  STAGE_NAME=>'MYSTAGE'));