-- see https://docs.snowflake.com/en/sql-reference/account-usage/task_versions

SELECT *
FROM snowflake.account_usage.task_versions
WHERE ROOT_TASK_ID = 'afb36ccc-. . .-b746f3bf555d' AND GRAPH_VERSION = 3;