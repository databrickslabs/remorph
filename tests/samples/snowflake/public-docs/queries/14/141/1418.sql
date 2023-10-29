-- see https://docs.snowflake.com/en/sql-reference/functions/system_convert_pipes_sqs_to_sns

SELECT SYSTEM$CONVERT_PIPES_SQS_TO_SNS(
   'my_s3_bucket', 'arn:aws:sns:us-east-2:111122223333:sns_topic');