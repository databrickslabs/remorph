-- see https://docs.snowflake.com/en/sql-reference/functions/get_stage_location

CREATE STAGE images_stage URL = 's3://photos/national_parks/us/yosemite/';

SELECT GET_STAGE_LOCATION(@images_stage);
