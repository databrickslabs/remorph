SELECT *
  FROM TABLE(information_schema.stage_directory_file_registration_history(
  STAGE_NAME=>'MYSTAGE'));