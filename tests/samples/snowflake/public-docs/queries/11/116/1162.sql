-- see https://docs.snowflake.com/en/sql-reference/functions/get_presigned_url

SELECT GET_PRESIGNED_URL(@images_stage, 'us/yosemite/half_dome.jpg', 3600);
