USE SCHEMA snowflake_sample_data.tpch_sf1;

SELECT APPROXIMATE_SIMILARITY(mh) FROM
    (
      (SELECT MINHASH(100, C5) mh FROM orders WHERE c2 <= 50000)
         UNION
      (SELECT MINHASH(100, C5) mh FROM orders WHERE C2 > 50000)
    );
