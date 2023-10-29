-- see https://docs.snowflake.com/en/sql-reference/functions/approximate_similarity

-- Record minhash information about only the new rows:
CREATE TABLE minhash_a_2 (mh) AS SELECT MINHASH(100, i) FROM ta WHERE i > 10;

-- Now combine all the minhash info for the old and new rows in table ta.
CREATE TABLE minhash_a (mh) AS
  SELECT MINHASH_COMBINE(mh) FROM
    (
      (SELECT mh FROM minhash_a_1)
      UNION ALL
      (SELECT mh FROM minhash_a_2)
    );