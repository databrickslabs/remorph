-- see https://docs.snowflake.com/en/sql-reference/functions/jarowinkler_similarity

SELECT s, t, JAROWINKLER_SIMILARITY(s, t), JAROWINKLER_SIMILARITY(t, s) FROM ed;
