-- see https://docs.snowflake.com/en/sql-reference/functions/minhash_combine

SELECT APPROXIMATE_SIMILARITY (mh) FROM
  (
    (SELECT mh FROM minhash_a)
    UNION ALL
    (SELECT mh FROM minhash_b)
  );