-- see https://docs.snowflake.com/en/sql-reference/functions/get_absolute_path

SELECT GET_ABSOLUTE_PATH(@images_stage, 'us/yosemite/half_dome.jpg');
