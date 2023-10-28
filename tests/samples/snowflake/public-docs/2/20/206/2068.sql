USE SCHEMA snowflake_sample_data.tpch_sf1;

SELECT MINHASH_COMBINE(mh) FROM
    (
      (SELECT MINHASH(5, c2) mh FROM orders WHERE c2 <= 10000)
        UNION
      (SELECT MINHASH(5, c2) mh FROM orders WHERE c2 > 10000 AND c2 <= 20000)
        UNION
      (SELECT MINHASH(5, C2) mh FROM orders WHERE c2 > 20000)
    );
