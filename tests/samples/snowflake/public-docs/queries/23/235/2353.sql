-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_aws_sns_iam_policy

select system$get_aws_sns_iam_policy('arn:aws:sns:us-west-2:001234567890:s3_mybucket');
