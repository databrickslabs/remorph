-- see https://docs.snowflake.com/en/sql-reference/functions/build_stage_file_url

SELECT BUILD_STAGE_FILE_URL(@images_stage,'/us/yosemite/half_dome.jpg');