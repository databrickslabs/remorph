-- see https://docs.snowflake.com/en/sql-reference/functions/get_relative_path

SELECT GET_RELATIVE_PATH(@images_stage, 's3://photos/national_parks/us/yosemite/half_dome.jpg');