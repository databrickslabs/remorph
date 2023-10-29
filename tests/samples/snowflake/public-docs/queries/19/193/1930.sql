-- see https://docs.snowflake.com/en/sql-reference/functions/approximate_jaccard_index

USE SCHEMA snowflake_sample_data.tpch_sf1;

SELECT APPROXIMATE_JACCARD_INDEX(mh) FROM
    (
      (SELECT MINHASH(100, C5) mh FROM orders WHERE c2 <= 50000)
         UNION
      (SELECT MINHASH(100, C5) mh FROM orders WHERE C2 > 50000)
    );
