-- presto sql:
select
  "json_extract"(params, '$.query') query,
  "json_extract"(params, '$.dependencies') IS NOT NULL AS TEST,
  "json_extract"(params, '$.dependencies') IS NULL AS TEST1,
  "json_extract"(params, '$.dependencies') AS TEST2
FROM
  drone_job_manager dm;

-- databricks sql:
SELECT
  params:query AS query,
  params:dependencies IS NOT NULL AS TEST,
  params:dependencies IS NULL AS TEST1,
  params:dependencies AS TEST2
FROM drone_job_manager AS dm
