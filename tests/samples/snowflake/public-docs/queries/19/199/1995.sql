-- see https://docs.snowflake.com/en/sql-reference/sql/show-columns

create or replace table dt_test (n1 number default 5, n2_int integer default n1+5, n3_bigint bigint autoincrement, n4_dec decimal identity (1,10),
                                 f1 float, f2_double double, f3_real real,
                                 s1 string, s2_var varchar, s3_char char, s4_text text,
                                 b1 binary, b2_var varbinary,
                                 bool1 boolean,
                                 d1 date,
                                 t1 time,
                                 ts1 timestamp, ts2_ltz timestamp_ltz, ts3_ntz timestamp_ntz, ts4_tz timestamp_tz);

show columns in table dt_test;
