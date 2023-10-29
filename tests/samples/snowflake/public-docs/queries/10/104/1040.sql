-- see https://docs.snowflake.com/en/sql-reference/functions/build_scoped_file_url

SELECT BUILD_SCOPED_FILE_URL(@images_stage,'/us/yosemite/half_dome.jpg');