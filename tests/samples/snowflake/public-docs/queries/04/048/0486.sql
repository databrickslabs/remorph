-- see https://docs.snowflake.com/en/sql-reference/functions/approximate_similarity

CREATE TABLE minhash_a_1 (mh) AS SELECT MINHASH(100, i) FROM ta;
CREATE TABLE minhash_b (mh) AS SELECT MINHASH(100, i) FROM tb;
CREATE TABLE minhash_c (mh) AS SELECT MINHASH(100, i) FROM tc;