-- see https://docs.snowflake.com/en/sql-reference/sql/alter-external-table

CREATE OR REPLACE STAGE mystage
  URL='<cloud_platform>://twitter_feed/logs/'
  .. ;

-- Create the external table
-- 'daily' path includes paths in </YYYY/MM/DD/> format
CREATE OR REPLACE EXTERNAL TABLE daily_tweets
  WITH LOCATION = @twitter_feed/daily/;

-- Refresh the metadata for a single day of data files by date
ALTER EXTERNAL TABLE exttable_part REFRESH '2018/08/05/';