SELECT APPROXIMATE_SIMILARITY (mh) FROM
  (
    (SELECT mh FROM minhash_a)
    UNION ALL
    (SELECT mh FROM minhash_c)
  );